#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/22 16:16
# @Author : hushaozhong
# @File : locust_test_01.py
# @Software: PyCharm
import datetime
import os
from gevent._semaphore import Semaphore
from locust import task, constant, events, FastHttpUser, SequentialTaskSet, TaskSet, HttpUser, LoadTestShape


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


class MyCustomShape(LoadTestShape):
    """
    时间段加载场景
    time -- 持续时间，  经过多少秒后，进入到下个阶段
    users -- 总用户数
    spawn_rate -- 产生率，即每秒启动/停止的用户数
    """
    stages = [
        {"time": 10, "users": 3, "spawn_rate": 10},
        {"time": 20, "users": 7, "spawn_rate": 10},
        {"time": 30, "users": 10, "spawn_rate": 10},
        {"time": 40, "users": 13, "spawn_rate": 10},
        {"time": 50, "users": 16, "spawn_rate": 10},
        {"time": 60, "users": 20, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage['time']:
                tick_data = (stage['users'], stage['spawn_rate'])
                return tick_data
        return None


# class StepLoadShaper(LoadTestShape):
#     """
#     逐步加载实例
#     step_time -- 逐步加载时间
#     step_load -- 用户每一步增加的量
#     spawn_rate -- 用户在每一步的停止/启动
#     time_limit -- 时间限制
#     """
#     setp_time = 30
#     setp_load = 10
#     spawn_rate = 10
#     time_limit = 60
#
#     def tick(self):
#         run_time = self.get_run_time()
#         if run_time > self.time_limit:
#             return None
#         current_step = math.floor(run_time / self.setp_time) + 1
#         return (current_step * self.setp_load, self.spawn_rate)


class TestDemo(SequentialTaskSet):

    @task
    def get_demo1(self):
        Semaphore().wait()  # 集合点等待并发
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
    wait_time = constant(0)


if __name__ == '__main__':
    os.system(f'locust -f locust_test_05.py')
