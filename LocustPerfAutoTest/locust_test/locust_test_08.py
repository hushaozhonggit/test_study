from locust import User, task, events, constant
import time
import websocket
import ssl
import json
import jsonpath
import pika


def eventType_success(request_type, eventType, recvText, total_time):
    events.request_success.fire(request_type=request_type,
                                name=eventType,
                                response_time=total_time,
                                response_length=len(recvText))


class rabbitMqPub(object):
    _locust_environment = None

    def __init__(self, host, port, username, passw):
        self.host = host
        self.port = port
        self.auth = pika.PlainCredentials(username, passw)

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port))

    def channel(self):
        self.channel = self.connection.channel()

    def basic_publish(self, queue, exchange, routing_key, body):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=body)

    def connect_close(self):
        self.connection.close()


class PublishUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(PublishUser, self).__init__(*args, **kwargs)
        self.client = rabbitMqPub(
            self.host, self.port, self.username, self.passw)
        self.client._locust_environment = self.environment


class ApiUser(PublishUser):

    host = '127.0.0.1'
    port = 5672
    username = 'guest'
    passw = 'guest'

    wait_time = constant(0.5)

    def on_start(self):

        # 与 rabbitMQ 建立连接
        start_time = time.time()
        self.client.connect()
        total_time = int(time.time() - start_time)
        eventType_success('Connect', self.host, '0', total_time)

        # 基于连接建立信道
        self.client.channel()

    def on_stop(self):
        self.client.connect_close()

    @task(1)
    def basic_publish(self):
        queue = 'TEST01'
        exchange = ''
        routing_key = 'TEST01'
        body = 'Hello World!'

        start_time = time.time()
        self.client.basic_publish(queue, exchange, routing_key, body)
        total_time = int(time.time() - start_time)
        eventType_success(queue, routing_key, body, total_time)
