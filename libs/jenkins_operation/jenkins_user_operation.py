from util.core import Operation
from libs.jenkins_api.jenkins_user_api import JenkinsUserAPI


class JenkinsUserOperation(Operation, JenkinsUserAPI):
    def get_all_usernames(self):
        r = self.asynch_people()
        # print(r.code)
        users = r.body.get("users")
        absolute_urls = [_['user']['absoluteUrl'] for _ in users]
        all_usernames = [_.split("/")[-1] for _ in absolute_urls]
        return all_usernames
