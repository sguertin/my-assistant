from abc import ABCMeta, abstractmethod
from datetime import time, timedelta, datetime
from pathlib import Path
from my_assistant.models.taskfile import TimeDayLog


class ITaskFileService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (
                hasattr(subclass, "get_time_log_path")
                and callable(subclass.get_time_log_path)
            )
            and (
                hasattr(subclass, "create_tracking_entry")
                and callable(subclass.create_tracking_entry)
            )
            and (
                hasattr(subclass, "get_last_entry_time")
                and callable(subclass.get_last_entry_time)
            )
            and (hasattr(subclass, "get_time_log") and callable(subclass.get_time_log))
            or NotImplemented
        )

    @abstractmethod
    def get_time_log_path(self, timestamp: datetime) -> Path:
        """Returns the file path of the time log for a given timestamp

        Args:
            timestamp (datetime): the date to retrieve the log file path for

        Returns:
            Path: path to logfile from timestamp
        """
        raise NotImplementedError

    @abstractmethod
    def get_time_log(self, timestamp: datetime) -> TimeDayLog:
        """Retrieves day's log for provided timestamp

        Args:
            timestamp (datetime): the date of the log to be retrieved

        Returns:
            TimeDayLog: The log for the provided timestamp
        """
        raise NotImplementedError

    @abstractmethod
    def create_tracking_entry(
        self, timestamp: datetime, entry: str, time_interval: timedelta
    ):
        """Add a new time tracking entry to the log file

        Args:
            timestamp (datetime): the timestamp of the tracking entry
            entry (str): The text entry
            time_interval (timedelta): how much time elapsed since the last entry
        """
        raise NotImplementedError

    @abstractmethod
    def get_last_entry_time(self, timestamp: datetime) -> time:
        """Returns the last entry from the log for the day of the provided timestamp

        Args:
            timestamp (datetime): date of the last entry

        Returns:
            time: the time the last entry was written
        """
        raise NotImplementedError
