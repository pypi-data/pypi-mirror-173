"""
iUAP HTTP auth protocol implementation
"""
import time
import math
import hashlib
import base64
import requests
from typing import Union, Tuple
from intelliw.config import config

try:
    import jwt
    has_jwt_package = True
except ImportError:
    print("[Framework Log] \033[33mIf want use authsdk, you need: pip install pyjwt\033[0m")
    has_jwt_package = False

requests.packages.urllib3.disable_warnings()


class Response:
    def __init__(self, status: int, body: str, error: Exception = None):
        self.status = status
        self.body = body
        self.error = error
        self.json = self._try_json()

    def raise_for_status(self):
        """
        raise :class:`IuapRequestException <IuapRequestException>` if status is not 200
        """
        if self.status != 200:
            msg = 'http request error, status: [{}], body: [{}] '.format(
                self.status, self.body)
            if self.error is not None:
                raise IuapRequestException(
                    msg + str(self.error)) from self.error
            raise IuapRequestException(msg)

    def _try_json(self):
        import json
        try:
            return json.loads(self.body)
        except:
            return None

    def __str__(self):
        return 'status: {}, body: {}, error: {}'.format(self.status, self.body, self.error)


class IuapRequestException(Exception):
    pass


def download(url, output_path, method="get", params=None, body=None, json=None, headers=None):
    # 加签
    token = sign(url, params)
    if headers is None:
        headers = {}
    headers['YYCtoken'] = token

    resp = sign_and_request(method=method, url=url,
                            body=body, params=params, json=json)
    resp.raise_for_status()
    mode = "wb"
    if type(resp.body) == str:
        mode = "w"
    with open(output_path, mode) as code:
        code.write(resp.body)


# stream_download 流式下载文件
def stream_download(url, output_path, method="get", params=None, body=None, json=None, headers=None):
    def plan_print(plan, speed):
        print("[Framework Log] dataset downloading: ", '{:.3f}'.format(plan), '%', '{:.3f}'.format(
            speed / (chunk_size ** 2)), 'MB/s', end='\r', flush=True)

    # 加签
    token = ""
    if has_jwt_package:
        token = ""
    if has_jwt_package:
        token = sign(url, params)


    if headers is None:
        headers = {}
    headers['YYCtoken'] = token

    # 请求下载地址，以流式的。打开要下载的文件位置。
    with requests.request(method=method, url=url, stream=True, verify=False, data=body, params=params, json=json) as r, open(output_path, 'wb') as file:
        total_size = int(r.headers['content-length'])
        chunk_size = 1024
        start_time = time.time()   # 请求开始的时间
        download_content_size = 0  # 下载的字节大小
        temp_size = 0              # 上秒的下载大小
        plan = 0                   # 进度下载完成的百分比

        # 开始下载每次请求chunk_size字节
        for content in r.iter_content(chunk_size=chunk_size):
            file.write(content)
            download_content_size += len(content)
            plan = (download_content_size / total_size) * 100
            if time.time() - start_time > 1:
                start_time = time.time()
                speed = download_content_size - temp_size
                plan_print(plan, speed)
                temp_size = download_content_size


def get(url: str, headers: dict = None, params: dict = None, timeout: Union[Tuple, int] = None) -> Response:
    """
    get request

    :param url: request url
    :param headers: request headers
    :param params: request url params
    :return: Response
    """
    return sign_and_request(url, 'GET', headers, params, timeout=timeout)


def post_json(url: str, headers: dict = None, params: dict = None, data: object = None, timeout: Union[Tuple, int] = None) -> Response:
    """
    post request, send data as json

    :param url: request url
    :param headers: request headers
    :param params: request url parameters
    :param data: request body. if data is not `str`, it will be serialized as json.
    :return: Response
    """

    if headers is None:
        headers = {}
    headers['Content-type'] = 'application/json; charset=UTF-8'
    return sign_and_request(url, 'POST', headers, params, json=data, timeout=timeout)


def put_file(url: str, headers: dict = None, params: dict = None, data: object = None, timeout: Union[Tuple, int] = None) -> Response:
    if headers is None:
        headers = {}
        headers['Content-type'] = 'application/octet-stream'
    return sign_and_request(url, 'PUT', headers, params, data, timeout=timeout)


def sign_and_request(url: str,
                     method: str = 'GET',
                     headers: dict = None,
                     params: dict = None,
                     body: dict = None,
                     json: dict = None,
                     sign_params: dict = None,
                     timeout: Union[Tuple, int] = None) -> Response:
    """
    sign and do request

    :param url: request url, without query
    :param method: Http request method, GET, POST...
    :param headers: request headers
    :param params: parameters will be sent as url parameters. Also used to generate signature if sign_params is None.
    :param body: request body
    :param sign_params: params used to generate signature, if sign_params is None, signature will be generated base on params.
    :return: response body
    """
    token = ""
    if has_jwt_package:
        token = sign(url, sign_params) if sign_params is not None else sign(
            url, params)

    if headers is None:
        headers = {}
    headers['YYCtoken'] = token

    return __do_request(url, method, headers, params, body, json, timeout=timeout)


def sign(url: str, params: dict) -> str:
    """
    generate iuap signature

    :param url: request url, without parameters
    :param headers: request headers
    :param params:  request parameters, x-www-form-urlencoded request's body parameters should also be included.
    :return: iuap signature
    """
    issue_at = __issue_at()
    sign_key = __build_sign_key(
        config.ACCESS_KEY, config.ACCESS_SECRET, issue_at, url)
    jwt_payload = {
        "sub": url,
        "iss": config.ACCESS_KEY,
        "iat": issue_at
    }
    if params is not None and len(params) > 0:
        sorted_params = sorted(params.items())
        for item in sorted_params:
            if item[1] is None:
                val = ''
            elif len(str(item[1])) >= 1024:
                val = str(__java_string_hashcode(str(item[1])))
            else:
                val = str(item[1])
            jwt_payload[item[0]] = val

    jwt_token = jwt.encode(jwt_payload, key=sign_key, algorithm='HS256')
    return str(jwt_token, encoding='UTF-8')


def __issue_at():
    issue_at = int(time.time())
    issue_at = math.floor(issue_at / 600) * 600
    return issue_at


def __build_sign_key(access_key, access_secret, access_ts, url):
    str_key = access_key + access_secret + str(access_ts * 1000) + url
    sign_key_bytes = hashlib.sha256(str_key.encode('UTF-8')).digest()
    return base64.standard_b64encode(sign_key_bytes).decode('UTF-8')


def __java_string_hashcode(s: str):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


def __do_request(url: str,
                 method: str = 'GET',
                 headers: dict = None,
                 params: dict = None,
                 data: dict = None,
                 json: dict = None,
                 timeout: Union[Tuple, int] = None) -> Response:

    for i in range(1, 5):
        try:
            resp = requests.request(
                method=method, url=url, params=params, data=data, json=json, headers=headers, verify=False, timeout=timeout)
            status_code = resp.status_code
            try:
                resp.encoding = "utf8"
                body = resp.content
            except UnicodeDecodeError:
                body = resp.content
            return Response(status_code, body)
        except requests.exceptions.RequestException as e:
            if i == 4:
                raise e
            time.sleep(i * 2)
            print(f"[request] request retry time: {i}, url: {url}")
