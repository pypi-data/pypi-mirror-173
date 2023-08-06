#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/17 17:34
# @Author  : xgy
# @Site    : 
# @File    : http_client.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import sys
import urllib

import requests
import json
from loguru import logger
from tqdm import tqdm


class HttpClient:

    def __init__(self):

        self.info_list = None
        self.info_download = None

    def get(self, url, **kw):
        params = kw
        res = requests.get(url, params=params)
        res_dict = json.loads(res.text)
        if res_dict["code"] == 200:
            self.info_list = res_dict
            return res_dict
        else:
            # raise IOError(self.error_msg(res_dict))
            self.error_msg(res_dict)
        # return res_dict

    def post(self, url, arg_type=None, **kw):
        if arg_type == "files":
            res = requests.post(url, files=kw)
        elif arg_type == "data":
            res = requests.post(url, data=kw)
        elif arg_type == "json":
            res = requests.post(url, json=kw)
        elif arg_type == "data/files":
            # 同时传文件和参数
            res = requests.post(url, files=kw["files"], data=kw["data"])
        elif arg_type is None:
            res = requests.post(url)
        else:
            raise KeyError("the arg_type for post should be in {}".format(['files', 'data', 'json', 'data/files']))

        res_dict = json.loads(res.text)
        if res_dict["code"] == 200:
            self.info_list = res_dict
            return res_dict
        else:
            self.error_msg(res_dict)

    def download(self, url, output=None, **kw):
        params = kw
        res = requests.post(url, data=params, stream=True)

        # 数据集存在性检验
        status_code = res.status_code
        if str(status_code) == '701':
            # raise Exception(json.loads(res.text))
            raise FileNotFoundError(json.loads(res.text)['msg'])

        total = int(res.headers.get('content-length', 0))

        # 获取头部信息
        disposition = str(res.headers.get('Content-Disposition'))
        # 截取头部信息文件名称
        filename = disposition.replace('attachment;filename=', '')

        # 转码
        filename = urllib.parse.unquote(filename)
        save_path = os.path.join(output, filename)

        # 添加保存路径
        with open(save_path, 'wb') as file, tqdm(desc=save_path, total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
            for data in res.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

        return save_path

    def error_msg(self, data):
        if data["code"] != 200:
            # print(data)
            error_code = data["code"]
            try:
                logger.error("error_code:{},message:{}", error_code, data["message"])
            except Exception:
                logger.error("error_code:{},message:{}", error_code, data["msg"])
            raise ConnectionError("Call server error")

    # def convert(self, url, method, arg_type, **kwargs):
    #     if method.upper() == "POST":
    #         if arg_type == "files":
    #             res = requests.post(url, files=kwargs)
    #         elif arg_type == "data":
    #             res = requests.post(url, data=kwargs)
    #         elif arg_type == "json":
    #             res = requests.post(url, json=kwargs)
    #         else:
    #             raise KeyError("the arg_type for post should be in {}".format(['files', 'data', 'json']))
    #     elif method.upper() == "GET":
    #         res = requests.get(url, params=kwargs)
    #     else:
    #         raise KeyError("the HTTP method should be POST or GET")
    #     res_dict = json.loads(res.text)
    #     self.error_msg(res_dict)
    #
    #     return res_dict


if __name__ == '__main__':
    print("start")
