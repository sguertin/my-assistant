from abc import ABCMeta, abstractmethod
from logging import Logger


class ILoggingFactory(ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_logger") and callable(subclass.get_logger)
        ) or NotImplemented

    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        """Retrieves a configured instance of the Logger class with the appropriate name

        Args:
            name (str): The name for the logger

        Returns:
            Logger: The configured logger
        """
        raise NotImplementedError()
