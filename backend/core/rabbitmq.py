import pika
import json
import base64
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    _instance = None

    def __init__(self):
        self.connection = None
        self.channel = None
        self._init_rabbitmq()

    # def __new__(cls):
    #     """Ensure a singleton instance is used."""
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #         cls._instance._init_rabbitmq()
    #     return cls._instance

    def _init_rabbitmq(self):
        """Initialize the RabbitMQ connection once."""
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(
                        settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
                    ),
                    heartbeat=600,  # Prevent idle disconnections
                    blocked_connection_timeout=300,
                    # virtual_host=settings.RABBITMQ_VHOST,
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)
            logger.info("RabbitMQ Publisher Connected Successfully")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"RabbitMQ Publisher Connection Error: {e}")
            self.connection, self.channel = None, None

    def _ensure_connection(self):
        """Ensure connection and channel are alive."""
        if self.connection is None or self.connection.is_closed:
            logger.warning(f"Reconnecting to RabbitMQ Publisher...")
            self._init_rabbitmq()
        elif self.channel is None or self.channel.is_closed:
            logger.warning("Reopening RabbitMQ Publisher channel...")
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)

    def publish_message(self, data):
        """Publish campaign data to RabbitMQ."""
        self._ensure_connection()

        if self.channel is None:
            logger.error("RabbitMQ Publisher: Cannot publish campaign, channel is None!")
            return

        try:
            # encoded_data = base64.b64encode(data).decode("utf-8")
            message = json.dumps(data)
            self.channel.basic_publish(
                exchange="",
                routing_key=settings.RABBITMQ_QUEUE_NAME,
                body=message,
            )
        except pika.exceptions.AMQPError as e:
            logger.error(f"RabbitMQ Publisher Error: {e}")
            self._init_rabbitmq()  # Only reinitialize if publishing fails

    def close_connection(self):
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
