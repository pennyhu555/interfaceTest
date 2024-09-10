import requests
from requests.auth import HTTPBasicAuth


class Response:
    def __init__(self,code,body,raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response

    def __repr__(self):
        return f"response code={self.code}\nresponse body={self.body}"


class RestClient:
    def __init__(self, base_url, username=None, api_token=None):
        self.base_url = base_url
        # 创建一个requests session
        self.s = requests.session()
        # 如果提供了用户名和API令牌，则设置身份验证
        if username and api_token:
            self.auth = HTTPBasicAuth(username, api_token)
        else:
            # 否则不使用身份验证
            self.auth = None

    def options(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        print(f"OPTIONS {endpoint}")
        r = self.s.options(endpoint, **kwargs)
        return self.process(r)

    def head(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        print(f"HEAD {endpoint}")
        r = self.s.head(endpoint, **kwargs)
        return self.process(r)

    def get(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        print(f"GET url={endpoint}")
        r = self.s.get(endpoint, auth=self.auth, **kwargs)
        # 不再直接返回原始响应内容，而是先调用process方法做处理
        return self.process(r)

    def post(self, endpoint, data=None, json=None,**kwargs):
        endpoint = self.base_url + endpoint
        print(f"POST {endpoint}")
        r = self.s.post(endpoint, data, json, **kwargs, auth=self.auth)
        return self.process(r)

    def put(self, endpoint, data=None, **kwargs):
        endpoint = self.base_url + endpoint
        print(f"PUT {endpoint}")
        r = self.s.put(endpoint, data, **kwargs, auth=self.auth)
        return self.process(r)

    def patch(self, endpoint, data=None, **kwargs):
        endpoint = self.base_url + endpoint
        print(f"PATCH {endpoint}")
        r = self.s.patch(endpoint, data, **kwargs, auth=self.auth)
        return self.process(r)

    def delete(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        print(f"DELETE {endpoint}")
        r = self.s.delete(endpoint, **kwargs, auth=self.auth)
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


class Jenkins:
    def __init__(self, base_url, username=None, api_token=None):
        # 使用restClient替代requests的session
        self.s = RestClient(base_url, username, api_token)
        self.use_jenkins = JenkinsOperation(self)

    def list_jobs(self, attribute_to_show='name'):
        response = self.s.get(f"/api/json?tree=jobs[{attribute_to_show}]")
        return response

    # 封装Jenkins的get user接口
    def get_user(self, username):
        response = self.s.get(f"/usr/{username}/api/json")
        return response


if __name__ == '__main__':
    username = 'admin'
    api_token = '1114f9db70dac50a1b30197718c5671c86'
    # 创建Jenkins类的一个实例
    anon = Jenkins(base_url='http://47.115.133.87:8080', username=username, api_token=api_token)
    # 调用封装好的方法列出所有job
    r = anon.list_jobs()
    print(r)
    if r:  # 确保 r 不为 None
        try:
            jobs = [_['name'] for _ in r.body['jobs'] if 'name' in _]
            print(f'jobs={jobs}')
        except KeyError as e:
            print(f"KeyError encountered: {e}")
            print(f"Full response: {r}")
    print(f"response code={r.code}")

    print('======================')
    rn = anon.use_jenkins.get_all_job_names()
    print(rn)
    rnu = anon.use_jenkins.get_all_job_names_with_url()
    print(rnu)