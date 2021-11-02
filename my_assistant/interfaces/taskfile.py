from datetime import datetime, timedelta, time


class ITaskFileService:

    def __init__(self, *args):
        raise TypeError('Interface ITaskFileService cannot be initialized')

    def create_tracking_entry(self, timestamp: datetime, entry: str, time_interval: timedelta) -> None:
        """Creates a new entry in the log file 

        Args:
            timestamp (datetime): The time of the recording
            entry (str): The entry contents
            time_interval (timedelta): The time interval
        """
        raise NotImplementedError("create_tracking_entry is not implemented")

    def get_last_entry_time(self, timestamp: datetime) -> time:
        """Retrieves the last recorded time in the log file for the date provided

        Args:
            timestamp (datetime): the date to check for a last entry date

        Returns:
            time: The time of the last entry
        """
        raise NotImplementedError("get_last_entry_time is not implemented")
