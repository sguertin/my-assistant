from datetime import time, timedelta, datetime
from pathlib import Path
from my_assistant.interfaces.base import Interface
from my_assistant.models.taskfile import TimeDayLog


class ITaskFileService(Interface):
    def get_time_log_path(self, timestamp: datetime) -> Path:
        """Returns the file path of the time log for a given timestamp

        Args:
            timestamp (datetime): the date to retrieve the log file path for

        Returns:
            Path: path to logfile from timestamp
        """
        pass

    def get_time_log(self, timestamp: datetime) -> TimeDayLog:
        """Retrieves day's log for provided timestamp

        Args:
            timestamp (datetime): the date of the log to be retrieved

        Returns:
            TimeDayLog: The log for the provided timestamp
        """
        pass

    def create_tracking_entry(self, timestamp: datetime, entry: str, time_interval: timedelta):
        """Add a new time tracking entry to the log file 

        Args:
            timestamp (datetime): the timestamp of the tracking entry
            entry (str): The text entry
            time_interval (timedelta): how much time elapsed since the last entry
        """
        pass

    def get_last_entry_time(self, timestamp: datetime) -> time:
        """Returns the last entry from the log for the day of the provided timestamp

        Args:
            timestamp (datetime): date of the last entry

        Returns:
            time: the time the last entry was written
        """
        pass
