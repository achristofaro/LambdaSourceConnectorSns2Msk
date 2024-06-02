import json
from confluent_kafka import Producer, KafkaException
from adapters.log.logger import Logger
from domain.interfaces.producer_interface import ProducerInterface
from .producer_config import KafkaConfig


class KafkaProducer(ProducerInterface):

    def __init__(self,):
        self._config = KafkaConfig()
        self._producer = Producer(**self._config.get_kafka_producer_config())
        self._topic = self._config.get_kafka_config()['topic']
        self._logger = Logger.configure_logging()

    def __acked(self, err, msg):
        if err is not None:
            self._logger.exception(f'Message delivery failed: {err}')
        else:
            self._logger.info(f'Message delivered to topic: {msg.topic()} [{msg.partition()}]')

    def produce(self, message):
        self._logger.info(f'Sending message: {message} to Topic: {self._topic}')

        try:
            msg_json_str = json.dumps({'data': message})
            self._producer.produce(
                self._topic,
                key=None,
                value=msg_json_str.encode('utf-8'),
                callback=self.__acked
            )
            self._producer.poll(0)

        except KafkaException as e:
            self._logger.exception(f'Kafka exception: {e}')
            raise KafkaException(e)

        except Exception as e:
            self._logger.exception(f'Unexpected error: {e}')
            raise Exception(e)

    def flush(self, timeout: float):
        self._producer.flush(timeout)
