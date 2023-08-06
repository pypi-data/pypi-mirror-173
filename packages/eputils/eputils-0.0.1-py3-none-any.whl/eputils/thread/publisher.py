from logging import Logger
from queue import Queue
from pika.channel import Channel
import pika
import threading

class PublisherThread(threading.Thread):
    PUBLISH_INTERVAL_SEC = 0.5
    RETRY_CONNECTION_INTERVAL = 3

    def __init__(self, host, creds_provider, exchange: str, queue: Queue, app_id: str, logger: Logger, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0
        self.exchange = exchange
        self._host = host
        self._creds_provider = creds_provider
        self._connection = None
        self._channel: Channel = None
        # self._entrance_event = threading.Event()
        self._logger = logger
        self._publisher_app_id = app_id
        self._publish_loop_started = False
        self._publish_queue: Queue = queue
        self._connected = threading.Event()
        self._publish_allow = False
        self._closing = False

    def connect(self):
        # if self._entrance_event.is_set(): return
        # self._entrance_event.set()

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
            self._call_later(self.publish_messages)
            pass
        except Exception as e:
            print(format(e))
    
    def _print(self, message):
        self._logger.info(f"{message} [thread {threading.get_ident()}]")

    def is_connected(self):
        return self._channel is not None and self._channel.is_open

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
        self._print(f"Connection CLOSED, error: {error}. Retrying in {PublisherThread.RETRY_CONNECTION_INTERVAL}..")
        # self._entrance_event.clear()
        # self._call_later(self._retry_connection, PublisherThread.RETRY_CONNECTION_INTERVAL)
        self._retry_connection()
    
    def on_connection_open_error(self, connection, error):
        self._print(f"Connection ERROR WHILE OPENING. Retrying in {PublisherThread.RETRY_CONNECTION_INTERVAL}..")
        # self._entrance_event.clear()
        self._call_later(self._retry_connection, PublisherThread.RETRY_CONNECTION_INTERVAL)
    
    def _retry_connection(self):
        if self._closing:
            self._print("Closing flag set, not retrying connection.")
            return

        self._print("Retrying to connect with message broker..")
        self.connect()

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
        
    def _call_later(self, func, after=PUBLISH_INTERVAL_SEC):
        self._connection.ioloop.call_later(
            after, 
            func)

    def _can_publish(self):
        return self.is_connected() and self._publish_allow

    def publish_messages(self):
        # self._print(f"checking for messages..")

        if self._closing:
            self._print("Thread closing, stopping publish message loop..")
            return

        if not self._can_publish():
            self._print("Cannot publish currently..")
            return self._call_later(self.publish_messages)
        
        while not self._publish_queue.empty():
            (message, routing_key) = self._publish_queue.get(block=False)
            self._print(f"publishing message to {routing_key}...")
        
            published = self.publish(
                message, 
                self.exchange, 
                routing_key)

            self._print(f"Published: {published}")

        return self._call_later(self.publish_messages)

    def close(self):
        self._logger.warning("Stopping publisher thread!")
        self._closing = True
        self._connection.close()
        # self._connection.ioloop.close()

    def run(self):
        self.connect()
        self._print("Starting io loop..")
        self._connection.ioloop.start()