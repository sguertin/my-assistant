
from logging import Logger


class ILoggingFactory:

    def get_logger(self, name: str) -> Logger:
        """Returns a fully configured logger with the name provided

        Args:
            name (str): the name for the logger

        Returns:
            Logger: The configured logger
        """
        pass
