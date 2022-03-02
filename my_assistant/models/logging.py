from enum import IntEnum
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG


class LogLevel(IntEnum):
    CRITICAL = CRITICAL
    ERROR = ERROR
    WARNING = WARNING
    INFO = INFO
    DEBUG = DEBUG
