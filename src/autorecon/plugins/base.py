from abc import ABC, abstractmethod

class PluginABC(ABC):
    @abstractmethod
    def accept(self, service: str, port: int) -> bool: ...
    @abstractmethod
    def run(self, target: str, port: int, config: dict) -> dict: ...
