#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/22 16:16
# @Author : hushaozhong
# @File : locust_test_01.py
# @Software: PyCharm
import math
import os
from locust import task, constant, events, FastHttpUser, SequentialTaskSet, TaskSet, HttpUser, LoadTestShape


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class DoubleWave(LoadTestShape):
    """
    自定义一个双波形图形，
    模拟在某两个时间点的最高值
    参数解析:
        min_users ： 最小用户数
        peak_one_users ： 用户在第一个峰值
        peak_two_users ： 用户在第二个峰值
        time_limit ： 测试执行总时间
    """
    min_users = 10  # 最小用户数
    peak_one_users = 30  # 第一个峰值的用户数
    peak_two_users = 50  # 第二个峰值的用户数
    time_limit = 60  # 测试执行时间

    def tick(self):
        run_time = round(self.get_run_time())
        if run_time < self.time_limit:
            user_count = (
                    (self.peak_one_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                    + (self.peak_two_users - self.min_users)
                    * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                    + self.min_users
            )
            return (round(user_count), round(user_count))
        else:
            return None


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
    host = "http://localhost:8888"
    tasks = [TestDemo]
    wait_time = constant(0)


if __name__ == '__main__':
    os.system('locust -f locust_test_06.py')
