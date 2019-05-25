import json
import pika
from threading import Thread

class Rabbit():

    function = None
    host = 'localhost'
    port = 5672
    userid = 'guest'
    password = 'guest'
    durable = True
    exchange = None
    queue = None
    routing_key = None

    def __init__(self, function, exchange, queue, routing_key=None, host=None, port=None, userid=None, password=None, durable=True):
        self.function = function
        self.exchange = exchange
        self.queue = queue
        self.routing_key = routing_key
        self.host = host or self.host
        self.port = port or self.port
        self.userid = userid or self.userid
        self.password = password or self.password
        self.durable = durable

    def connect(self):
        credentials = pika.PlainCredentials(self.userid, self.password)
        parameters = pika.ConnectionParameters(self.host, self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def disconnect(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

    def declare(self):
        self.channel.exchange_declare(self.exchange, exchange_type='direct', durable=self.durable)
        self.channel.queue_declare(queue=self.queue, durable=self.durable)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=self.routing_key)

    def _consume(self, ch, method, properties, body):
        try:
            self.function.run(body)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print('Processing error. Message not acknoledged.', e, '\n', str(self.function), '\nBody:', str(body))

    def consume(self):
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self._consume, 
        )
        try:
            self.channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print('RabbitMQ connection error')
            self.connect()
            self.consume()
