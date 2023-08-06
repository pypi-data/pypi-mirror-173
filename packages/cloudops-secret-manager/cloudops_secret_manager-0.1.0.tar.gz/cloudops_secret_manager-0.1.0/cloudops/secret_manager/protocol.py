from typing import Protocol


class SecretManagerProtocol(Protocol):
    def pull(self) -> dict:
        ...

    def push(self, payload: dict) -> None:
        ...
