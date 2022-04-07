from logging import Logger
from abc import ABCMeta, abstractmethod


class ILoggingFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_logger")
            and callable(subclass.get_logger)
            or NotImplemented
        )

    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        """Returns a fully configured logger with the name provided

        Args:
            name (str): the name for the logger

        Returns:
            Logger: The configured logger
        """
        raise NotImplementedError
