from util.core import Operation, Result
from libs.jenkins_api.jenkins_job_api import JenkinsJobAPI


class JenkinsJobOperation(Operation, JenkinsJobAPI):
    def get_all_job_names(self):
        r = self.list_jobs("name")
        jobs = [_['name'] for _ in r.body['jobs']]
        return jobs

    # 封装Jenkins的业务方法-获取所有job的名称和地址
    def get_all_job_names_with_url(self):
        r = self.list_jobs("name,url")
        jobs = {_['name']: _['url'] for _ in r.body['jobs']}
        return jobs

    # 封装Jenkins的业务方法-创建job
    def create_job_with_dsl(self, dsl, job_name):
        result = Result()
        r = self.get_job(job_name)
        if r.code == 200:
            result.success = False
            result.info = "Job Already Exist"
            return result
        script = f"""def jobDSL=\"\"\"{dsl}\"\"\";
    def flowDefinition = new org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition(jobDSL, true);
    def parent = Jenkins.instance;
    def job = new org.jenkinsci.plugins.workflow.job.WorkflowJob(parent, "{job_name}")
    job.definition = flowDefinition
    job.save();
    Jenkins.instance.reload()"""
        self.run_groovy(script)
        r = self.get_job (job_name)
        if r.code == 200 and r.body.get("displayName") == job_name:
            result.success = True
            result.info = f"Job Created at {r.body.get ('url')}"
            return result
        else:
            result.success = False
            result.info = f"Job={job_name} Created Failed"
            return result

    # 封装Jenkins的业务方法-删除job
    def delete_all_jobs(self):
        names = self.get_all_job_names()
        names.remove("interfaceTest")
        for name in names:
            self.delete_job(name)
        newnames = self.get_all_job_names()
        return Result(newnames == [], f"{newnames} still not be deleted")
