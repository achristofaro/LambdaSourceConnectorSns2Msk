from abc import ABC, abstractmethod

from domain.entities.message import Message


class PublishInterface(ABC):

    @abstractmethod
    def publish(self, message: Message) -> None:
        raise NotImplementedError
