from typing import Any

from domain.interfaces.producer_interface import ProducerInterface
from domain.interfaces.publish_interface import PublishInterface


class PublishMessage(PublishInterface):
    def __init__(self, producer: ProducerInterface) -> None:
        self._producer = producer

    def publish(self, message: Any):
        self._producer.produce(message)
