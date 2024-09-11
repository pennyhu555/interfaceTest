from requests.auth import HTTPBasicAuth
from libs.jenkins_api.jenkins_job_api import JenkinsJobAPI
from libs.jenkins_api.jenkins_user_api import JenkinsUserAPI
from libs.jenkins_operation.jenkins_job_operation import JenkinsJobOperation
from libs.jenkins_operation.jenkins_user_operation import JenkinsUserOperation
from util import logger
from util.core import RestClient


class Jenkins(JenkinsJobOperation, JenkinsUserOperation):
    def __init__(self, base_url, username=None, api_token=None):
        # 使用restClient替代requests的session
        self.base_url = base_url
        self.rest_client = RestClient(base_url)
        self.job_api = JenkinsJobAPI(self)
        self.user_api = JenkinsUserAPI(self)
        self.crumb_field_name = None
        self.crumb_field_value = None
        # 在初始化时增加登入的机制
        if username and api_token:
            self.login(username, api_token)

    def login(self, username, api_token):
        logger.info(f"login username={username}")
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

    def run_groovy(self, script):
        payload = {'script': script}
        response = self.rest_client.post(f"/scriptText", data=payload)
        return response


if __name__ == '__main__':
    # 创建Jenkins类的一个实例
    admin = Jenkins('http://47.115.133.87:8080', 'admin',
                    '1114f9db70dac50a1b30197718c5671c86')
    job_dsl = """properties([parameters([string(name:'Run', defaultValue:'Yes',
                description:'a parameter')])])node {stage("test"){echo 'Hello World'}}"""
    # 可以直接调用各个模块里封装的api
    # 调用JenkinsJobAPI里封装的方法
    r = admin.job_api.list_jobs ()  # TODO 通过根节点成员变量来调用“叶子节点的方法”。
    print(r)
    r = admin.list_jobs ()  # TODO 通过根节点继承的“叶子节点的方法”直接调用。与上面的方式等价。
    print(r)
    # 调用JenkinsUserAPI里封装的方法
    r = admin.user_api.get_user ("admin")  # TODO 通过根节点成员变量来调用“叶子节点的方法”。
    print(r)
    r = admin.get_user ("admin")  # TODO 通过根节点继承的“叶子节点的方法”直接调用。与上面的方式等价。
    print(r)
    # 可以直接调用各种operations里的方法，仍旧自动打日志
    # 调用JenkinsUserOperations里的方法
    admin.get_all_usernames()

    # 调用JenkinsJobOperations里的方法
    admin.job_api.delete_job("testjob0001")
    admin.create_job_with_dsl(job_dsl, "testjob0001")
    admin.create_job_with_dsl(job_dsl, "testjob0001")
    admin.job_api.delete_job("testjob0001")

    # 通过禁止重定向修复bug
    # 再次调用JenkinsUserOperations里的方法，这次成功了耶
    admin.get_all_usernames()
