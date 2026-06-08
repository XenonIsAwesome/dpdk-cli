from abc import ABC, abstractmethod
from typing import List


class Installer(ABC):
    @staticmethod
    @abstractmethod
    def install(packages: List[str]):
        raise NotImplementedError()
