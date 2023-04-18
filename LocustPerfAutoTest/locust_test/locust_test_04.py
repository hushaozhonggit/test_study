#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/22 16:16
# @Author : hushaozhong
# @File : locust_test_01.py
# @Software: PyCharm
import datetime
import os
from gevent._semaphore import Semaphore
from locust import task, constant, events, FastHttpUser, SequentialTaskSet, TaskSet, HttpUser


def on_hatch_complete(**kwargs):
    # 创建集合点，当locust实例产生完成时触发（即用户启动完毕）
    Semaphore().acquire()
    Semaphore().release()  # 抛出钩子


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')
    events.spawning_complete.add_listener(on_hatch_complete)  # 挂载到钩子函数


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class TestDemo(SequentialTaskSet):
    def on_start(self):
        print("前置任务")

    def on_stop(self):
        print("任务后置")

    @task
    def get_demo1(self):
        Semaphore().wait()  # 集合点等待并发
        body = {"username": "ECS的mock接口1测试"}
        with self.client.get("/get/test/one/demo_api?", params=body, catch_response=True) as resp:
            if resp.elapsed.total_seconds() < 3:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + resp.text)


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8888"
    tasks = [TestDemo]
    # wait_time = constant(3)


if __name__ == '__main__':
    # os.system("locust -f locust_test_04.py")
    os.system("locust -f locust_test_04.py -u 5 -r 1 -t 3s")
