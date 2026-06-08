from abc import abstractmethod, ABC


class BaseCommand(ABC):
    @staticmethod
    @abstractmethod
    def add_subparser(subparsers):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def handle(subparsers):
        raise NotImplementedError()
