import logging
import logging.config
from logging import Logger

from my_assistant.constants import LogLevel


class LoggingFactory:
    log_level: LogLevel

    def __init__(self, log_level: LogLevel):
        self.log_level = log_level
        logging.basicConfig(
            level=LogLevel.CRITICAL,
            format="%(name)-15s %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
        )

    def get_logger(self, name: str) -> Logger:
        log = logging.getLogger(name)
        log.setLevel(self.log_level)
        return log
