import json
from uuid import uuid4
from confluent_kafka import Producer, KafkaException
from confluent_kafka.serialization import StringSerializer
from adapters.log.logger import Logger
from domain.interfaces.producer_interface import ProducerInterface
from .producer_config import KafkaConfig


class KafkaProducer(ProducerInterface):

    def __init__(self):
        self._config = KafkaConfig()
        self._producer = Producer(**self._config.get_kafka_producer_config())
        self._topic = self._config.get_kafka_config().get('topic')
        self._logger = Logger.get_logger()
        self._string_serializer = StringSerializer('utf_8')
        
    def __acked(self, err, msg):
        if err is not None:
            self._logger.exception(f'Delivery failed for message {msg.key()}: {err}')
            return
        else:
            self._logger.info(
                f'Message {msg.key()} successfully produced to topic {msg.topic()} [{msg.partition()}] at offset {msg.offset()}'
            )

    def produce(self, message):
        self._logger.info(f'Sending message to topic {self._topic}')

        try:
            msg_json_str = json.dumps({'data': message})
            self._producer.produce(
                self._topic,
                key=self._string_serializer(str(uuid4())),
                value=msg_json_str.encode('utf-8'),
                callback=self.__acked
            )
            self._producer.poll(0.0)

        except KafkaException as e:
            self._logger.exception(f'Kafka exception: {e}')
            raise

        except Exception as e:
            self._logger.exception(f'Unexpected error: {e}')
            raise

    def flush(self, timeout: float):
        self._producer.flush(timeout)
