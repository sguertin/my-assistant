import logging
import logging.config
from logging import Logger
from typing import Optional

from my_assistant.constants import LogLevel
from my_assistant.interfaces.logging import ILoggingFactory
from my_assistant.models.settings import Settings


class LoggingFactory(ILoggingFactory):
    settings: Settings

    def __init__(self, settings: Optional[Settings]):
        if settings is None:
            settings = Settings.load()
        self.settings = settings
        logging.basicConfig(
            level=LogLevel.CRITICAL,
            format="%(name)-15s %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
        )

    def get_logger(self, name: str) -> Logger:
        log = logging.getLogger(name)
        log.setLevel(self.settings.log_level)
        return log
