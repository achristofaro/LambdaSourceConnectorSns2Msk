from domain.interfaces.publish_interface import PublishInterface
from entities.message import Message


class PublishMessage(PublishInterface):
    def __init__(self, publisher: PublishInterface):
        self._publisher = publisher

    def publish(self, message: Message):
        self._publisher.publish(message)
