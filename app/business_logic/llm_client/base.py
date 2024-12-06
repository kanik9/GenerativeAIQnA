from typing import Any
from abc import ABC, ABCMeta, abstractmethod


class BaseLLM(ABC, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def _llm_client(self) -> None:
        pass

    @abstractmethod
    def create(self) -> Any:
        pass