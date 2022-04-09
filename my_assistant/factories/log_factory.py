import logging
import logging.config
from logging import Logger

from rich.logging import RichHandler

from my_assistant.constants import LogLevel
from my_assistant.interfaces.factories.log_factory import ILoggingFactory


class LoggingFactory(ILoggingFactory):
    _log_level: LogLevel

    def __init__(self, log_level: LogLevel):
        self._log_level = log_level
        logging.basicConfig(
            datefmt="[%Y-%m-%d %H:%M:%S]",
            format="%(message)s",
            handlers=[RichHandler(rich_tracebacks=True)],
            level=LogLevel.NOTSET,
        )

    def update_level(self, log_Level: LogLevel):
        self._log_level = log_Level

    def get_logger(self, name: str) -> Logger:
        log = logging.getLogger(name)
        log.setLevel(self._log_level)
        return log
