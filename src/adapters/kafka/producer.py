import json
from typing import Any
from uuid import uuid4

from confluent_kafka import KafkaException, Producer, cimpl
from confluent_kafka.serialization import StringSerializer

from adapters.log.logger import Logger
from use_cases.interfaces.producer_interface import ProducerInterface

from .producer_config import KafkaConfig


class KafkaProducer(ProducerInterface):

    def __init__(self) -> None:
        self.__config = KafkaConfig()
        self.__producer = Producer(**self.__config.get_kafka_producer_config())
        self.__topic = self.__config.get_kafka_config().get("topic")
        self.__logger = Logger.get_logger()
        self.__string_serializer = StringSerializer("utf_8")

    def __acked(self, err: str, msg: cimpl.Message) -> None:
        if err is not None:
            self.__logger.exception(f"Delivery failed for message {msg.key()}: {err}")
            return
        else:
            self.__logger.info(
                f"Message {msg.key()} successfully produced to topic {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
            )

    def produce(self, message: Any) -> None:
        self.__logger.info(f"Sending message to topic {self.__topic}")

        try:
            # Serialize message
            msg_json_str = json.dumps({"data": message}).encode("utf-8")

            self.__producer.produce(
                self.__topic,
                key=self.__string_serializer(str(uuid4())),
                value=msg_json_str,
                callback=self.__acked,
            )
            self.__producer.poll(0.0)

        except KafkaException as e:
            self.__logger.exception(f"Kafka exception: {e}")
            raise

        except Exception as e:
            self.__logger.exception(f"Unexpected error: {e}")
            raise

    def flush(self, timeout: float) -> None:
        self.__producer.flush(timeout)

    def len(self) -> int:
        return len(self.__producer)
