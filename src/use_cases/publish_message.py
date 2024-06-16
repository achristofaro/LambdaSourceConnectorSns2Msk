from typing import Any

from .interfaces.producer_interface import ProducerInterface
from .interfaces.publish_interface import PublishInterface


class PublishMessage(PublishInterface):
    def __init__(self, producer: ProducerInterface) -> None:
        self.__producer = producer

    def publish(self, message: Any):
        self.__producer.produce(message)
