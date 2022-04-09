import logging
import logging.config
from logging import Logger

from rich.logging import RichHandler

from my_assistant.constants import LogLevel
from my_assistant.interfaces.logfactory import ILoggingFactory
from my_assistant.models.settings import SettingsService


class LoggingFactory(ILoggingFactory):
    log_level: LogLevel

    def __init__(self, log_level: LogLevel):
        self.log_level = log_level
        logging.basicConfig(
            datefmt="[%Y-%m-%d %H:%M:%S]",
            format="%(message)s",
            handlers=[RichHandler(rich_tracebacks=True)],
            level=LogLevel.NOTSET,
        )

    def get_logger(self, name: str) -> Logger:
        log = logging.getLogger(name)
        log.setLevel(self.log_level)
        return log
