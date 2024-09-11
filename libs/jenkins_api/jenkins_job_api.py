class JenkinsJobAPI():
    def __init__(self, jenkins):
        self.jenkins = jenkins
        self.rest_client = jenkins.rest_client

    def list_jobs(self,attribute_to_show="name"):
        return self.rest_client.get(f"/api/json?tree=jobs[{attribute_to_show}]")

    def get_job(self,job):
        return self.rest_client.get(f"/job/{job}/api/json")

    def delete_job(self, job_name):
        return self.rest_client.post(f"/job/{job_name}/doDelete", allow_redirects=False)
