#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/9/27 9:29
# @Author  : xgy
# @Site    : 
# @File    : model_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import sys

import click
from csp.command.cli import csptools


# 一级命令 CSPtools topic
@csptools.group("topic")
def topic():
    """
    主题命令，包括主题信息列表、主题下载等子命令

    \b
    csp topic 'commands' -h 获取子命令使用帮助
    """


## 模型信息列表展示
@topic.command()
@click.option("-m", "--more", type=click.BOOL, help="是否以 linux more 命令风格查看结果", default=True, show_default=True)
@click.option("-n", "--name", type=click.STRING, help="主题名称，支持模糊查找", required=True, default='', show_default=True)
@click.option("-c", "--classify", type=click.STRING, help="主题分类，支持模糊查找", required=True, default='', show_default=True)
def list(name, classify, more):
    """
    主题列表命令

    \b
    使用示例：csp topic list
    """
    from csp.topic.topic_server import topic_list
    res = topic_list(name, classify, show=more)

    if more:
        os.makedirs("/tmp", exist_ok=True)
        if sys.platform == "win32":
            code = "GBK"
        else:
            code = "utf-8"

        with open("/tmp/topic_l.txt", "w", encoding=code) as fw:
            fw.write(res)
        txt_abs = os.path.abspath("/tmp/topic_l.txt")

        os.system("more " + txt_abs)

    else:
        print(res)


@topic.command()
@click.option("-n", "--name", type=click.STRING, help="主题名称，支持模糊查找", required=True)
@click.option("-o", "--output", type=click.STRING, help="下载保存目录", required=True)
def download(name, output):
    """
    主题下载命令

    \b
    使用示例：csp topic download -n "主题名称" -o "下载保存目录"
    """
    try:
        from csp.topic.topic_server import topic_download
        save_path = topic_download(name, output)
        print("下载完成，文件保存至：{}".format(save_path))
    except Exception as ae:
        print(repr(ae))


# @topic.command()
# @click.option("-i", "--tar_path", type=click.STRING, help="模型镜像文件（.tar）路径", required=True)
# def upload(tar_path):
#     """
#     模型镜像上传命令
#
#     \b
#     使用示例：csp topic upload -i "模型镜像文件（.tar）路径"
#     """
#     from csp.topic.topic_server import model_upload
#     model_upload(tar_path)


# @topic.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称，支持模糊查找", required=True)
# def start(name):
#     """
#     模型服务启动命令
#
#     \b
#     使用示例：csp topic start
#     """
#     from csp.topic.topic_server import model_start
#     model_start(name)


# @topic.command()
# @click.option("-n", "--name", type=click.STRING, help="模型名称，支持模糊查找", required=True)
# def eva(name):
#     """
#     模型评估命令
#
#     \b
#     使用示例：csp topic eva
#     """
#     from csp.topic.topic_server import model_eva
#     model_eva()


if __name__ == '__main__':
    print("start")
