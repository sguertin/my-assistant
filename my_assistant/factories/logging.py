import logging
import logging.config
from logging import Logger, CRITICAL

from models.settings import Settings


class LoggingFactory:

    def __init__(self, settings: Settings):
        self.settings = settings
        logging.basicConfig(
            level=CRITICAL,
            format='%(name)-15s %(message)s',
            datefmt='[%Y-%m-%d %H:%M:%S]',
        )

    def get_logger(self, name: str) -> Logger:
        log = logging.getLogger(name)
        log.setLevel(self.settings.log_level)
        return log
