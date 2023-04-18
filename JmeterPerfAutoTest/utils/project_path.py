#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 23:00
# @Author  : hushaozhong
# @File    : project_path.py
# @Software: PyCharm
import os


def get_root_path():
    """
    功能：获取项目所在的根目录
    代码逻辑：
        (1)获取当前py文件的系统路径
        (2)获取路径分隔符（操作系统不同），分隔符为 \ 或者 /
        (3)本项目名称是Ecs开头，获取Ecs字符串在路径的下标，方便截取
        (4)使用Ecs的下标截取，得到项目所在的根路径
        (5)返回根路径
    :return: 返回根路径
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    if "/" in current_path:
        separator = "/"
    else:
        separator = "\\"
    index = current_path.find("Ecs")
    temp = current_path[index:]
    project_name = temp[:temp.find(separator)]
    root_path = current_path[:current_path.find(project_name + separator)+len(project_name + separator)]
    return root_path


def get_path(path=None):
    """
    功能：获取path路径的完整的路径，包括盘符
    :param path: 入参，部分路径,需要处理分隔符
    :return: 返回全路径（包含根路径）
    """
    root_path = get_root_path()
    if "/" in root_path:
        path.replace("\\", "/")
    elif "\\" in root_path:
        path.replace("/", "\\")
    complete_path = os.path.abspath(get_root_path() + path)
    return complete_path


def mkdir(p):
    """
    功能：创建文件夹
    :param p: 目标路径地址
    :return:
    """
    try:
        from pathlib import Path
        path = Path(p)
        if not path.is_dir():
            path.mkdir()
    except Exception as e:
        print("指定路径不存在，创建报错，报错信息：{}".format(str(e)))
        os.makedirs(p)
        print("逐级创建路径文件夹完成")
        return


def get_filename(path):
    """
    功能：截取全路径中尾部的文件名称
    :param path:
    :return:
    """
    filename = str()
    if "/" in path:
        path_list = path.split("/")
        path_list_new = [i for i in path_list if i != '']
        filename = path_list_new[len(path_list_new) - 1]
    elif "\\" in path:
        path_list = path.split("\\")
        path_list_new = [i for i in path_list if i != '']
        filename = path_list_new[len(path_list_new) - 1]
    if "." in filename:
        return filename.strip()
    else:
        return "{}不是文件".format(filename)


# print(get_root_path())
# get_path(get_root_path())
get_filename(get_root_path())
