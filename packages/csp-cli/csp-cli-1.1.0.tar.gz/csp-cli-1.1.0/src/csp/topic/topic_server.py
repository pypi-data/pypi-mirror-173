#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/27 8:52
# @Author  : xgy
# @Site    : 
# @File    : model_server.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os
import re

from csp.aip.common.http_client import HttpClient
from csp.common.config import Configure
from csp.common.utils import format


def format_table(string):
    """
    优化model list 输出格式
    Parameters
    ----------
    string

    Returns
    -------

    """
    s_l_copy = []
    s_l = string.split("\n")
    for index, item in enumerate(s_l):
        s_l_copy.append(item)

        # 判断字符串起始位置特征
        pattern_start = r'^\|\s*\|'
        result_start = re.match(pattern_start, item, flags=re.S)
        if result_start:
            len_start = len(result_start.group())
            # 第一格 分割线 替换
            if s_l[index - 1].startswith("+----"):
                res = s_l[index - 1].replace("-", " ", len_start - 2)
                res = "|" + res[1:]
            else:
                res = s_l[index - 1]

            # s_l_copy[index - 1] = res

            # 第二格至第五格 分割线 替换
            j = 0
            for i in range(len_start - 1, len(res)):
                if res[i] == "-":
                    res = res[:i] + " " + res[i + 1:]
                if res[i] == "+":
                    res = res[:i] + "|" + res[i + 1:]
                    j += 1
                if j >= 5:
                    break

            # 最后一格 分割线 替换
            pattern_end = r"\+[\-]*\+$"
            result_end = re.search(pattern_end, s_l[index - 1], flags=re.S)
            if result_end:
                len_end = len(result_end.group())
                s_rep = "| "
                for i in range(len_end - 3):
                    s_rep += " "
                s_rep = s_rep + "|"
                res = re.sub(pattern_end, s_rep, res)

            s_l_copy[index - 1] = res

    string_new = "\n".join(s_l_copy)

    return string_new


def drop_list(res):
    """
    list 接口返回结果处理
    Parameters
    ----------
    res

    Returns
    -------

    """
    res_n = {"data": []}
    res_data = res["data"]
    for item in res_data:
        ms_detail_list = item["msDetailList"]
        if not ms_detail_list:
            item_n = {"classifyName": item["classifyName"],
                      "modelName": item["modelName"],
                      "modelVersion": item["modelVersion"],
                      "status": item["status"],
                      "serviceUrl": item["serviceUrl"],
                      "module": "",
                      "datasetNames": "",
                      "modeScores": "",
                      "serviceDesc": item["serviceDesc"],
                      }
            res_n["data"].append(item_n)
        else:
            for index, model in enumerate(ms_detail_list):
                if index == 0:
                    item_n = {"classifyName": item["classifyName"],
                              "modelName": item["modelName"],
                              "modelVersion": item["modelVersion"],
                              "status": item["status"],
                              "serviceUrl": item["serviceUrl"],
                              "module": model["module"],
                              "datasetNames": model["datasetNames"],
                              "modeScores": model["modeScores"],
                              "serviceDesc": item["serviceDesc"],
                              }
                else:
                    item_n = {"classifyName": "",
                              "modelName": "",
                              "modelVersion": "",
                              "status": "",
                              "serviceUrl": "",
                              "module": model["module"],
                              "datasetNames": model["datasetNames"],
                              "modeScores": model["modeScores"],
                              "serviceDesc": "",
                              }
                res_n["data"].append(item_n)

    return res_n


def topic_list(name='', class_name='', show=True):
    interface_config = Configure().data
    http_client = HttpClient()

    url = interface_config["list"]["model"]
    params = {"modelName": name, "classifyName": class_name}
    res_dict = http_client.get(url, **params)

    res_dict = drop_list(res_dict)

    title_dict = {"主题": "classifyName", "服务名称": "modelName", "版本号": "modelVersion",
                  "状态": "status", "服务地址": "serviceUrl", "功能": "module", "关联数据集": "datasetNames",
                  "评分": "modeScores", "服务描述": "serviceDesc"}

    x = format(res_dict, title_dict, show=show)
    x_string = x.get_string()
    x_string = format_table(x_string)

    return x_string


def topic_download(name, output):
    interface_config = Configure().data
    http_client = HttpClient()

    os.makedirs(output, exist_ok=True)

    url = interface_config["download"]["model"]
    params = {"name": name}
    save_path = http_client.download(url, output, **params)

    return save_path


# def model_upload(file_path):
#     pass
#     import requests
#     from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
#
#     file_name = os.path.basename(file_path)
#
#     def my_callback(monitor):
#         progress = (monitor.bytes_read / monitor.len) * 100
#         print("\r 文件上传进度：%d%%(%d/%d)"
#               % (progress, monitor.bytes_read, monitor.len), end=" ")
#
#     e = MultipartEncoder(
#         fields={'model': (file_name, open(file_path, 'rb'), 'application/octet-stream')}
#     )
#
#     m = MultipartEncoderMonitor(e, my_callback)
#     interface_config = Configure().data
#
#     url = interface_config["upload"]["model"]
#
#     r = requests.post(url, data=m, headers={'Content-Type': m.content_type})
#     print(r.text)


# def model_start(name):
#     interface_config = Configure().data
#     http_client = HttpClient()
#
#     url = interface_config["start"]["model"]
#     params = {"modelName": name}
#     res_dict = http_client.post(url, **params)


# def model_eva():
#     pass


if __name__ == '__main__':
    print("start")
