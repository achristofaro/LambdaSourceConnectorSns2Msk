import socket

from helpers.config import ConfigLoader


class KafkaConfig:
    def __init__(self):
        self.__config = ConfigLoader().get_config()
        self.__kafka_config = self.__config.get("KAFKA", {})
        self.__aws_config = self.__config.get("AWS", {})

    def get_kafka_config(self) -> dict[str, str]:
        return self.__kafka_config

    def get_kafka_producer_config(self) -> dict[str, object]:
        return {
            "bootstrap.servers": self.__kafka_config.get("bootstrap_servers"),
            "client.id": f"{self.__kafka_config.get('client_id')}: {socket.gethostname()}",
            "socket.timeout.ms": 1000,  # Socket timeout in milliseconds
            "socket.keepalive.enable": True,  # Enable TCP keepalive for idle connections
            "api.version.request": True,  # Request API version from Kafka broker
            "batch.num.messages": 100,  # Maximum number of messages in batch before sending
            "linger.ms": 5,  # Maximum time in milliseconds to wait before sending a batch of messages
            "batch.size": 32 * 1024,  # Maximum batch size in bytes
            "compression.type": "gzip",  # Compression type for messages
            "message.max.bytes": 8 * 1024,  # Maximum size of a message in bytes
            "acks": "all",  # Number of replica acknowledgments required before considering the message as sent
            "enable.idempotence": True,  # Ensures that messages are delivered exactly once
            "max.in.flight.requests.per.connection": 5,  # Maximum number of unacknowledged messages per connection
            "retries": 3,  # Maximum number of resend attempts in case of failure
            "retry.backoff.ms": 300,  # Waiting time between resend attempts in milliseconds
            "delivery.timeout.ms": 120000,  # Maximum time to attempt to deliver a message
        }
