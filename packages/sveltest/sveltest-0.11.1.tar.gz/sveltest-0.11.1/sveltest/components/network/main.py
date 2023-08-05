#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2022/10/20

import json
import requests
from requests import (Request,Session)
from typing import Optional, List, Union, Sequence, Dict, overload, Tuple

from sveltest.components._test_core import request_env
from sveltest.support.common import ObjectDict

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# 内置环境控制
#
class RequestBase(object):

    def __init__(self):

        self.encoding = None

    @request_env()
    def get(self, router: Optional[str],
            data: Optional[Dict]=None,
            proxies:Optional[Dict]=None,
            # 对SSL证书认证
            verify:Sequence[bool]=False,
            env_control:Sequence[bool]=True,
            allow_redirects:Sequence[bool]=False,
            timeout:Optional[Union[int,float]]=None,
            cookies:Optional[Dict]=None,
            headers:Optional[Union[Dict,bool]]=False,
            # 客户端的证书
            cert:Optional[Union[str,Tuple[str,str]]]=None
            ):
        """

        """

        if headers is False:
            self.headers_data = self.get.Header
        else:
            self.get.Header.update(headers)


        if router and env_control is True:
            self.__request_module = requests.get(
                url=self._join(router), params=data, proxies=proxies,
                verify=verify, allow_redirects=allow_redirects, timeout=timeout, cookies=cookies,cert=cert,
                headers=self.headers_data
            )

        else:
            self.__request_module = requests.get(
                url=router, params=data, proxies=proxies, verify=verify,allow_redirects=allow_redirects,timeout=timeout,
                cookies=cookies,headers=self.headers_data,cert=cert,
            )

        return self


    @request_env()
    def post(self, router: Optional[str],
            data: Optional[Dict]=None,
            proxies:Optional[Dict]=None,
            # 对SSL证书认证
            verify:Sequence[bool]=False,
            env_control:bool=True,
            allow_redirects:Sequence[bool]=False,
            timeout:Optional[Union[int,float]]=None,
            cookies:Optional[Dict]=None,
            headers:Optional[Union[Dict,bool]]=False,
            # 客户端的证书
            cert:Optional[Union[str,Tuple[str,str]]]=None
            ):
        """

        """


        if headers is False:
            self.headers_data = self.post.Header
        else:
            self.post.Header.update(headers)

        self.headers_data = self.post.Header

        try:
            _req_data = json.dumps(data) if self.headers_data["Content-Type"] == "application/json" else data

        except:
            _req_data = data

        if router and env_control is True:
            self.__request_module = requests.post(
                url=self._join(router), data=_req_data, proxies=proxies,
                verify=verify, allow_redirects=allow_redirects,
                timeout=timeout, cookies=cookies,cert=cert,
                headers=self.headers_data
            )

        else:
            self.__request_module = requests.post(
                url=router, data=_req_data, proxies=proxies,
                verify=verify,allow_redirects=allow_redirects,timeout=timeout,
                cookies=cookies,headers=self.headers_data,cert=cert,
            )

        return self




    def upload_file(self,file:Optional[Union[List[str],str]]):
        """
        上传文件
        """
        if isinstance(file,str):
            with open('massive-body', 'rb') as f:
                requests.post('http://some.url/streamed', data=f)

        if isinstance(file,list):

            multiple_files = [
                ('images', ('foo.png', open(x, 'rb'), 'image/png'))
                for x in file
            ]
            requests.post('url', files=multiple_files)

        return self



    def put(self, router: Optional[str],
            data: Optional[Dict]
            ):
        """

        """

        if router:
            self.__request_module = requests.get(url=self._join(router), params=data)

            return self



    def code_ok(self):
        return self.__request_module.codes.ok


    def delete(self, router: Optional[str],
            data: Optional[Dict]
               ):
        """

        """

        if router:
            self.__request_module = requests.get(url=self._join(router), params=data)

            return self



    def patch(self, router: Optional[str],
            data: Optional[Dict]):
        """

        """

        if router:
            self.__request_module = requests.patch(url=self._join(router), params=data)

            return self

    @property
    def request_url(self):
        """

        """
        return self.__request_module.request.url

    @property
    def url(self):
        """

        """
        return self.__request_module.url

    @request_env()
    def _join(self, router):
        """

        """
        return '/'.join([self._join.backend_env_host, router])


    @property
    def content(self):
        """

        """
        return self.__request_module.content

    @property
    def text(self):
        """

        """

        return self.__request_module.text

    @property
    def json(self):
        """

        """
        return self.__request_module.json()


    def encoding_(self,coding:Optional[str]="utf-8"):
        """

        """
        self.__request_module.encoding = coding
        return self

    def save_image(self,content:Optional[bytes],fp:Optional[open]):
        """

        """
        from PIL import Image
        from io import BytesIO

        img = Image.open(BytesIO(content))
        img.save(fp=fp)
        return self

    @property
    def request_header(self):
        return HttpRequestHeaders(self.__request_module.request.headers)

    @property
    def request_headers(self):
        return self.__request_module.request.headers


    @property
    def header(self):
        """
        查看请求头
        """
        return HttpResponseHeaders(self.__request_module.headers)

    @property
    def headers(self):
        """
        查看请求头
        """
        return self.__request_module.headers


    @property
    def headers_obj(self):
        """
        查看请求头
        """
        return ObjectDict(self.__request_module.headers)

    @property
    def history(self):
        """
        查看请求头
        """
        return self.__request_module.history

    @property
    def status_code(self):
        """
        查看请求头
        """
        return self.__request_module.status_code



class HttpResponseHeaders:

    def __init__(self,obj:Optional[object]):
        self.obj = obj

    @property
    def content_type(self):
        """"""
        return self.obj["Content-Type"]

    @property
    def connection(self):
        """"""
        return self.obj["Connection"]

    @property
    def content_length(self):
        """"""
        return self.obj["Content-Length"]

    @property
    def keep_alive(self):
        """"""
        return self.obj["Content-Length"]

    @property
    def server(self):
        """"""
        return self.obj["Server"]

    @property
    def permissions_policy(self):
        """"""
        return self.obj["permissions-policy"]

    @property
    def last_modified(self):
        """"""
        return self.obj["Last-Modified"]

    @property
    def access_control_allow_origin(self):
        """"""
        return self.obj["Access-Control-Allow-Origin"]
    @property
    def date(self):
        """"""
        return self.obj["Date"]

    @property
    def strict_transport_security(self):
        """"""
        return self.obj["Strict-Transport-Security"]

    @property
    def etag(self):
        """"""
        return self.obj["ETag"]

    @property
    def expires(self):
        """"""
        return self.obj["expires"]

    @property
    def cache_control(self):
        """"""
        return self.obj["Cache-Control"]

    @property
    def x_proxy_cache(self):
        """"""
        return self.obj["x-proxy-cache"]

    @property
    def accept_encoding(self):
        """"""
        return self.obj["x-proxy-cache"]

class HttpRequestHeaders:

    def __init__(self,obj:Optional[object]):
        self.obj = obj

    @property
    def content_type(self):
        """"""
        return self.obj["Content-Type"]

    @property
    def connection(self):
        """"""
        return self.obj["Connection"]

    @property
    def content_length(self):
        """"""
        return self.obj["Content-Length"]

    @property
    def keep_alive(self):
        """"""
        return self.obj["Content-Length"]

    @property
    def server(self):
        """"""
        return self.obj["Server"]

    @property
    def permissions_policy(self):
        """"""
        return self.obj["permissions-policy"]

    @property
    def last_modified(self):
        """"""
        return self.obj["Last-Modified"]

    @property
    def access_control_allow_origin(self):
        """"""
        return self.obj["Access-Control-Allow-Origin"]
    @property
    def date(self):
        """"""
        return self.obj["Date"]

    @property
    def strict_transport_security(self):
        """"""
        return self.obj["Strict-Transport-Security"]

    @property
    def etag(self):
        """"""
        return self.obj["ETag"]

    @property
    def expires(self):
        """"""
        return self.obj["expires"]

    @property
    def cache_control(self):
        """"""
        return self.obj["Cache-Control"]

    @property
    def x_proxy_cache(self):
        """"""
        return self.obj["x-proxy-cache"]

    @property
    def accept_encoding(self):
        """"""
        return self.obj["x-proxy-cache"]





# https://sveltest-team.github.io/docs/logo.png


if __name__ == '__main__':

    r = RequestBase()
    data= {
    "username":13453001,"password":123456
    }
    ret = r.post("http://127.0.0.1:8666/api/v1/login",data=data,headers={"data":'666'},env_control=False).encoding_()
    # data = requests.post("http://127.0.0.1:8666/api/v1/login",headers={"data":'666'},)
    # print(data.json)
    print(ret.json)
    # print(data.header.connection)
    # print(data.headers)


    # print(data.status_code == data.code_ok)


