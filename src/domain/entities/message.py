from typing import Any, Type, TypeVar

T = TypeVar("T", bound="Message")


class Message:

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def validate(self) -> None:
        if not isinstance(self._data, dict):
            raise ValueError("Message must be a dictionary")

    @classmethod
    def from_json(cls: Type[T], json_data: dict[str, Any]) -> T:
        # Converts a JSON to a Message instance.
        return cls(data=json_data)

    def to_json(self) -> dict[str, Any]:
        # Converts the Message instance to a JSON.
        return {"data": self._data}

    def __str__(self) -> str:
        return self.__dict__.__str__()
