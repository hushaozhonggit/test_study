from locust import events

# 模块级别为这些事件设置侦听器：在测试开始或停止时运行一些代码


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is ending")

