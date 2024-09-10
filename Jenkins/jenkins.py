# import textwrap
import requests
from requests.auth import HTTPBasicAuth
import datetime, threading, shutil, os
from datetime import datetime, timezone, timedelta


def clear_log():
    shutil.rmtree("logs", True)
    os.mkdir("logs")


class MyLog:
    def __init__(self,log_level="INFO"):
        self.INFO = 1
        self.DEBUG = 2
        log_dict = {"INFO":self.INFO, "DEBUG":self.DEBUG}
        self.log_level = log_dict[log_level]

    def info(self,msg):
        msg = msg.replace (u'\xa0', u' ')  # 解决编码问题，gbk里没有\xa0，用空格替代
        timezone_offset = 8.0   # 将日志的时区设置为东八区
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = "UnNamed Scenario"
        if self.log_level >= self.INFO:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt","a") as f:
            f.write(f"[{timestamp}]{msg}\n")

    def debug(self, msg):
        msg = msg.replace(u'\xa0', u' ')   # 解决编码问题，gbk里没有\xa0，用空格替代
        timezone_offset = 8.0   # 将日志的时区设置为东八区
        tzinfo = timezone(timedelta(hours=timezone_offset))
        timestamp = datetime.now(tzinfo)
        try:
            scenario_name = threading.current_thread().scenario_name
        except:
            scenario_name = "UnNamed Scenario"
        if self.log_level >= self.DEBUG:
            print(f"[{scenario_name}][{timestamp}]{msg}")
        with open(f"logs//logs_{scenario_name}.txt", "a") as f:
            f.write(f"[{timestamp}]{msg}\n")


class Response:
    def __init__(self,code,body,raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response
        self.print_raw_request(raw_response)

    def __repr__(self):
        # 打印原始响应的状态码和响应体内容
        return f"response code={self.code}\n response body={self.body}"

    # 自动打出所有通过rest_client发送的请求的原始请求和原始响应
    def print_raw_request(self, response):
        format_headers = lambda d: '\n'.join(f'{k}:{v}' for k, v in d.items())
        # logger.info("{req.method} {req.url} {req.body}".format(req=response.request))
        # logger.info("{res.status_code} {res.text}".format(res=response))
        req = response.request
        res = response
        reqhdrs = format_headers(response.request.headers)
        reshdrs = format_headers(response.headers)
        logger.debug(f'''
        ---------------request---------------
        {req.method} {req.url}
        {reqhdrs}
        
        {req.body if req.body else ""}
        ---------------response---------------
        {res.status_code} {res.reason} {res.url}
        {reshdrs}
        
        {res.text if res.text else ""}
        ---------------end---------------
        ''')


class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url
        # 创建一个requests session
        self.s = requests.Session()

    def options(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"OPTIONS {endpoint}")
        r = self.s.options(endpoint, **kwargs)
        return self.process(r)

    def head(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"HEAD {endpoint}")
        r = self.s.head(endpoint, **kwargs)
        return self.process(r)

    def get(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"GET url={endpoint}")
        r = self.s.get(endpoint, **kwargs)
        # 不再直接返回原始响应内容，而是先调用process方法做处理
        return self.process(r)

    def post(self, endpoint, data=None, json=None,**kwargs):
        endpoint = self.base_url + endpoint
        # print(f"POST {endpoint}")
        r = self.s.post(endpoint, data, json, **kwargs)
        return self.process(r)

    def put(self, endpoint, data=None, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"PUT {endpoint}")
        r = self.s.put(endpoint, data, **kwargs)
        return self.process(r)

    def patch(self, endpoint, data=None, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"PATCH {endpoint}")
        r = self.s.patch(endpoint, data, **kwargs)
        return self.process(r)

    def delete(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"DELETE {endpoint}")
        r = self.s.delete(endpoint, **kwargs)
        return self.process(r)

    def process(self, response):
        # 获取http响应中的状态码
        code = response.status_code
        # 获取http响应中的响应体内容
        try:
            # 尝试解析响应中的json
            body = response.json()
        except:
            # 如果解析失败则直接把响应中的content内容返回
            body = str(response.content)
        # 新建Response类对象作为返回值
        return Response(code, body, response)


class Result():
    def __init__(self, info=""):
        self.success = True
        self.info = info

    def __repr__(self):
        # 打印信息
        return f"success={self.success}:{self.info}"


# jenkinsOperation类将原来Jenkins类中的业务操作代码分离出来
class JenkinsOperation:
    def __init__(self, jenkins):
        self.jenkins = jenkins

    # 封装Jenkins的业务方法-获取所有job名称
    def get_all_job_names(self):
        r = self.jenkins.list_jobs("name")
        jobs = [_['name'] for _ in r.body['jobs']]
        return jobs

    # 封装Jenkins的业务方法-获取所有job的名称和地址
    def get_all_job_names_with_url(self):
        r = self.jenkins.list_jobs("name,url")
        jobs = {_['name']: _['url'] for _ in r.body['jobs']}
        return jobs

    # 封装Jenkins的业务方法-创建job
    def create_job_with_dsl(self, dsl, job_name):
        result = Result()
        r = self.jenkins.get_job(job_name)
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
        self.jenkins.run_groovy(script)
        r = self.jenkins.get_job(job_name)
        if r.code == 200 and r.body.get("displayName") == job_name:
            result.success = True
            result.info = f"Job Created at {r.body.get('url')}"
            return result
        else:
            result.success = False
            result.info = f"Job={job_name} Created Failed"
            return result

    # 封装Jenkins的业务方法-删除job
    def delete_all_jobs(self):
        names = self.get_all_job_names()
        for name in names:
            self.jenkins.delete_job(name)
        return Result(f"{names} all deleted")


class Jenkins:
    def __init__(self, base_url, username=None, api_token=None):
        # 使用restClient替代requests的session
        self.base_url = base_url
        self.rest_client = RestClient(base_url)
        self.use_jenkins = JenkinsOperation(self)
        self.crumb_field_name = None
        self.crumb_field_value = None
        # 在初始化时增加登入的机制
        if username and api_token:
            self.login(username, api_token)

    def login(self, username, api_token):
        self.rest_client.s.auth = HTTPBasicAuth(username,api_token)
        r = self.get_crumber_issuer()
        if r.code == 200:
            try:
                self.crumb_field_name = r.body['crumbRequestField']
                self.crumb_field_value = r.body['crumb']
                # 在session中设置crumb的字段名和值
                self.rest_client.s.headers[self.crumb_field_name] = self.crumb_field_value
                return self
            except KeyError as er:
                print(f"KeyError encountered:{er}")
                print(f"full response body:{r.body}")
        else:
            print(f"failed to receive crumb. Status code:{r.code}, Response:{r.body}")

    def logout(self):
        del self.rest_client.s.headers[self.crumb_field_name]
        self.rest_client.auth = None
        self.crumb_field_name = None
        self.crumb_field_value = None

    def get_crumber_issuer(self):
        response = self.rest_client.get("/crumbIssuer/api/json")
        return response

    def list_jobs(self, attribute_to_show='name'):
        response = self.rest_client.get(f"/api/json?tree=jobs[{attribute_to_show}]")
        return response

    # 封装Jenkins的get user接口
    def get_user(self, username):
        response = self.rest_client.get(f"/usr/{username}/api/json")
        return response

    def run_groovy(self, script):
        payload = {'script': script}
        response = self.rest_client.post(f"/scriptText", data=payload)
        return response

    def get_job(self,job):
        response = self.rest_client.get(f"/job/{job}/api/json")
        return response

    def delete_job(self, job_name):
        response = self.rest_client.post(f"/job/{job_name}/doDelete")
        return response


if __name__ == '__main__':
    clear_log()
    logger = MyLog()
    # 创建Jenkins类的一个实例
    admin = Jenkins('http://47.115.133.87:8080', 'admin',
                    '1114f9db70dac50a1b30197718c5671c86')
    job_dsl = """properties([parameters([string(name:'Run', defaultValue:'Yes',
                description:'a parameter')])])node {stage("test"){echo 'Hello World'}}"""
    r = admin.list_jobs ()
    print(r)