#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/22 16:16
# @Author : hushaozhong
# @File : locust_test_01.py
# @Software: PyCharm
import os
from locust import task, constant, events, FastHttpUser, SequentialTaskSet, TaskSet, HttpUser


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class TestDemo(SequentialTaskSet):

    @task
    def get_demo1(self):
        body = {"username": "ECS的mock接口1测试"}
        with self.client.get("/get/test/one/demo_api?", params=body, catch_response=True) as resp:
            if resp.elapsed.total_seconds() < 3:
                print(resp.json())

    def on_start(self):
        print("前置任务")

    def on_stop(self):
        print("任务后置")


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8888"
    tasks = [TestDemo]
    # wait_time = constant(0.5)


if __name__ == '__main__':
    os.system("locust -f locust_test_02.py")
