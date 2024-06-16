from abc import ABC, abstractmethod

from domain.entities.message import Message


class ProducerInterface(ABC):

    @abstractmethod
    def produce(self, message: Message) -> None:
        raise NotImplementedError
