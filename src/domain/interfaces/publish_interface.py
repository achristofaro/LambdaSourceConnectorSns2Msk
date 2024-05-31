from abc import ABC, abstractmethod
from entities.message import Message


class PublishInterface(ABC):

    @abstractmethod
    def publish(self, message: Message) -> None:
        raise NotImplementedError
