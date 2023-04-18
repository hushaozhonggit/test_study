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


class rabbitMqSub(object):
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

    def subscribe(self, queue):
        self.channel.queue_declare(queue='TEST01')

        for method_frame, properties, body in self.channel.consume('TEST01'):
            # 显示消息部分并确认消息
            # print(method_frame, properties, body)
            self.channel.basic_ack(method_frame.delivery_tag)

            return body

    def connect_close(self):
        requeued_messages = self.channel.cancel()
        print('Requeued %i messages' % requeued_messages)
        self.connection.close()


class subscribeUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(subscribeUser, self).__init__(*args, **kwargs)
        self.client = rabbitMqSub(
            self.host, self.port, self.username, self.passw)
        self.client._locust_environment = self.environment


class ApiUser(subscribeUser):
    host = '127.0.0.1'
    port = 5672
    username = 'guest'
    passw = 'guest'

    wait_time = constant(0)

    def on_start(self):
        start_time = time.time()
        self.client.connect()
        total_time = int(time.time() - start_time)
        eventType_success('Connect', self.host, '0', total_time)

        start_time = time.time()
        self.client.channel()
        total_time = int(time.time() - start_time)
        eventType_success('Channel', self.host, '0', total_time)

    def on_stop(self):
        self.client.connect_close()

    @task(1)
    def subscribe(self):
        queue = 'TEST01'

        start_time = time.time()
        body = self.client.subscribe(queue)
        total_time = int(time.time() - start_time)
        eventType_success('[RECV]', queue, body, total_time)
