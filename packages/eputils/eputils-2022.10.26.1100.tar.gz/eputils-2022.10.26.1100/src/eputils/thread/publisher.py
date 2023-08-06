from logging import Logger
from queue import Queue
from typing import Callable
from pika.channel import Channel
from .abstract import AbstractThread
from .settings import ConnectionSettings
import pika
import threading

class PublisherThread(AbstractThread):
    def __init__(self, 
                 host: str, 
                 creds_provider: Callable[[], (str, str)], 
                 exchange: str, 
                 publish_queue: Queue, 
                 app_id: str, 
                 logger: Logger,
                 settings: ConnectionSettings = ConnectionSettings.default()):
        super().__init__(host, creds_provider, logger, settings)

        self.exchange = exchange
        self._publisher_app_id = app_id
        self._publish_loop_started = False
        self._publish_queue: Queue = publish_queue
        self._connected = threading.Event()
        self._publish_allow = False

    def connect(self):
        self._print(f"OPENING connection for publisher at host {self._host}...")
        creds_user, creds_pass = self._creds_provider()
        credentials = pika.PlainCredentials(creds_user, creds_pass)

        self._connection = pika.SelectConnection(
            pika.ConnectionParameters(
                host=self._host,
                credentials=credentials),
            on_open_callback=self.on_connection_open,
            on_close_callback=self.on_connection_close,
            on_open_error_callback=self.on_connection_open_error)

        try:
            self._call_later(self.publish_messages, self._settings.loop_interval)
            pass
        except Exception as e:
            self._print_error(format(e))

    def publish(self, message, exchange, routing_key):
        if not self.is_connected():
            self._print("Could not publish: NO CONNECTION")
            return False

        props = pika.BasicProperties(app_id=self._publisher_app_id,
                                     content_type="application/json")

        self._channel.basic_publish(exchange=exchange,
                                    routing_key=routing_key,
                                    body=message,
                                    properties=props,
                                    mandatory=True)
        
        self._print(f"published to {routing_key}")

        return True
    
    def on_connection_open(self, connection):
        self._print("Connection OPENED")
        self._print("Making channel..")
        self._connection.channel(
            on_open_callback=self.on_channel_open)
    
    def on_connection_close(self, connection, error):
        self._print(f"Connection CLOSED, error: {error}. Retrying..")
        self._retry_connection()
    
    def on_connection_open_error(self, connection, error):
        self._print(f"Connection ERROR WHILE OPENING. Retrying in {self._settings.retry_connection_interval}..")
        self._call_later(self._retry_connection, self._settings.retry_connection_interval)

    def on_channel_open(self, channel: Channel):
        self._channel = channel
        self._channel.add_on_return_callback(self.on_return)
        self._channel.add_on_close_callback(self.on_channel_close)
        self._print("Channel opened")

        if self.exchange != "":
            self._print("Declaring exchange..")
            self._channel.exchange_declare(exchange=self.exchange, 
                                           exchange_type="direct", 
                                           callback=self.on_exchange_declared)
        else: self._publish_allow = True

    def on_channel_close(self, channel, reason: Exception):
        self._print(f"Channel closed with reason: {reason}")

    def on_exchange_declared(self, connection):
        self._print("Exchange declared")
        self._publish_allow = True
        self._connected.set()

    def on_return(self, channel, method, properties, body):
        self._print(f"Message got returned!")

        queue_name = method.routing_key
        exchange = method.exchange
        message = body
        self._print(f"Fixing routing for {queue_name} in exchange {exchange}..")
        self.__declare_route_and_queue_and_resend(exchange, queue_name, message)
    
    def __declare_route_and_queue_and_resend(self, exchange, queue_name, message):
        def __queue_bound(_):
            self._publish_queue.put((message, queue_name))
            self._print(f"Bound and republished message")

        def __queue_declared(_):
            self._print(f"Binding new queue and route {queue_name}..")
            self._channel.queue_bind(queue_name, exchange, queue_name, callback=__queue_bound)

        self._print(f"Declaring new queue and route {queue_name}..")
        self._channel.queue_declare(queue_name, durable=True, exclusive=False, callback=__queue_declared)

    def _can_publish(self):
        return self.is_connected() and self._publish_allow

    def publish_messages(self):
        if self._stop_event.is_set():
            self._print("Thread closing, stopping publish message loop..")
            self._close()
            return

        if not self._can_publish():
            self._print("Cannot publish currently..")
            return self._call_later(self.publish_messages, self._settings.loop_interval)
        
        while not self._publish_queue.empty():
            (message, routing_key) = self._publish_queue.get(block=False)
            self._print(f"publishing message to {routing_key}...")
        
            published = self.publish(
                message, 
                self.exchange, 
                routing_key)

            self._print(f"Published: {published}")

        return self._call_later(self.publish_messages, self._settings.loop_interval)