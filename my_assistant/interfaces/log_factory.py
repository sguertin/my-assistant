from logging import Logger
from abc import ABCMeta, abstractmethod


from abc import ABCMeta, abstractmethod
from logging import Logger

from my_assistant.constants import LogLevel


class ILoggingFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "get_logger") and callable(subclass.get_logger))
            and (hasattr(subclass, "update_level") and callable(subclass.update_level))
            or NotImplemented
        )

    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        """Retrieves a configured instance of the Logger class with the appropriate name

        Args:
            name (str): The name for the logger

        Returns:
            Logger: The configured logger
        """
        raise NotImplementedError()

    @abstractmethod
    def update_level(self, log_level: LogLevel) -> None:
        """Updates the default log level for the factory

        Args:
            log_level (LogLevel): The new log level to be used as the default

        """
        raise NotImplementedError()
