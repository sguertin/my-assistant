from datetime import datetime, timedelta, time


class ITaskFileService:
    def create_tracking_entry(self, timestamp: datetime, entry: str, time_interval: timedelta) -> None:
        """[summary]

        Args:
            timestamp (datetime): [description]
            entry (str): [description]
            time_interval (timedelta): [description]
        """
        pass

    def get_last_entry_time(self, timestamp: datetime) -> time:
        pass
