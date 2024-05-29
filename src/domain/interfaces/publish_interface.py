from abc import ABC, abstractmethod


class PublishInterface(ABC):

    @abstractmethod
    def publish(self, message) -> None:
        raise NotImplementedError
