#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/22 16:16
# @Author : hushaozhong
# @File : locust_test_01.py
# @Software: PyCharm
import json
import os
from jsonpath import jsonpath
from locust import task, constant, events, FastHttpUser, SequentialTaskSet, TaskSet, HttpUser


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class TestDemo(SequentialTaskSet):

    def get_demo1(self):
        pass

    @task
    def post_demo1(self):
        hed = {"sign": self.sign, "param": self.param}
        body = {"username": self.username}
        with self.client.post("/post/test/one/demo_api", headers=hed, data=json.dumps(body),
                              catch_response=True) as resp:
            if resp.status_code == 200:
                print(resp.json())


    @task
    def post_demo2(self):
        hed = {"sign": self.sign, "param": self.param}
        body = {"username": self.username}
        with self.client.post("/post/test/two/demo_api", headers=hed, data=json.dumps(body),
                              catch_response=True) as resp:
            if resp.elapsed.total_seconds() < 3:
                print(resp.json())

    @task
    def post_demo3(self):
        hed = {"sign": self.sign, "param": self.param}
        body = {"username": self.username}
        with self.client.post("/post/test/three/demo_api", headers=hed, data=json.dumps(body),
                              catch_response=True) as resp:
            if resp.status_code == 200:
                print(resp.json())

    @task
    def post_demo4(self):
        hed = {"sign": self.sign, "param": self.param}
        body = {"username": self.username}
        with self.client.post("/post/test/four/demo_api", headers=hed, data=json.dumps(body),
                              catch_response=True) as resp:
            if resp.status_code == 200:
                print(resp.json())

    def on_start(self):
        print("前置任务")
        body = {"username": "ECS的mock接口1测试"}
        with self.client.get("/get/test/one/demo_api?", params=body, catch_response=True) as resp:
            if resp.elapsed.total_seconds() < 3:
                self.param = jsonpath(resp.json(), "$..supplier")[0]
                self.username = jsonpath(resp.json(), "$..supplierName")[0]
                self.sign = jsonpath(resp.json(), "$.traceId")[0]
                print(self.sign, self.param, self.username)

    def on_stop(self):
        print("任务后置")


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8888"
    tasks = [TestDemo]
    wait_time = constant(3)


if __name__ == '__main__':
    os.system("locust -f locust_test_01.py")
