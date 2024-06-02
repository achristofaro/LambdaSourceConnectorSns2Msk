from domain.interfaces.publish_interface import PublishInterface
from domain.interfaces.producer_interface import ProducerInterface
from entities.message import Message


class PublishMessage(PublishInterface):
    def __init__(self, producer: ProducerInterface):
        self._producer = producer

    def publish(self, message: Message):
        self._producer.produce(message)
