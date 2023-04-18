#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/14 15:13
# @Author : hushaozhong
# @File : __init__.py
# @Software: PyCharm
from locust import events
from locust.runners import MasterRunner
# 该init事件在每个 Locust 进程开始时触发。在分布式模式中特别有用，其中每个工作进程都需要进行一些初始化


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")
        # ssss