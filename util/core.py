import requests
from util import logger


class Response:
    def __init__(self, code, body, raw_response):
        self.code = code
        self.body = body
        self.raw_response = raw_response
        self.print_history(raw_response)
        self.print_raw_request(raw_response)

    def __repr__(self):
        # 打印原始响应的状态码和响应体内容
        return f"response code={self.code}\n response body={self.body}"

    def print_history(self, response):
        for r in response.history:
            self.print_raw_request(r)

    # 自动打出所有通过rest_client发送的请求的原始请求和原始响应
    def print_raw_request(self, response):
        format_headers = lambda d: '\n'.join (f'{k}:{v}' for k, v in d.items())
        # logger.info("{req.method} {req.url} {req.body}".format(req=response.request))
        # logger.info("{res.status_code} {res.text}".format(res=response))
        req = response.request
        res = response
        reqhdrs = format_headers (response.request.headers)
        reshdrs = format_headers (response.headers)
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
        r = self.s.options (endpoint, **kwargs)
        return self.process (r)

    def head(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"HEAD {endpoint}")
        r = self.s.head (endpoint, **kwargs)
        return self.process (r)

    def get(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"GET url={endpoint}")
        r = self.s.get (endpoint, **kwargs)
        # 不再直接返回原始响应内容，而是先调用process方法做处理
        return self.process (r)

    def post(self, endpoint, data=None, json=None, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"POST {endpoint}")
        r = self.s.post (endpoint, data, json, **kwargs)
        return self.process (r)

    def put(self, endpoint, data=None, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"PUT {endpoint}")
        r = self.s.put (endpoint, data, **kwargs)
        return self.process (r)

    def patch(self, endpoint, data=None, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"PATCH {endpoint}")
        r = self.s.patch (endpoint, data, **kwargs)
        return self.process (r)

    def delete(self, endpoint, **kwargs):
        endpoint = self.base_url + endpoint
        # print(f"DELETE {endpoint}")
        r = self.s.delete (endpoint, **kwargs)
        return self.process (r)

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


class Operation:
    def __getattribute__(self, item):
        func = super().__getattribute__(item)
        if type(func) == type(logger.info):
            def log(*args, **kwargs):
                r = func(*args, **kwargs)
                if not isinstance(r, Response):
                    logger.info(f"{func.__name__} -> {r}")
                return r
            return log
        else:
            return func
