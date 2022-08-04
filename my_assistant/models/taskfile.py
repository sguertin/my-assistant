from dataclasses import dataclass
from datetime import datetime, time

from dataclasses_json import DataClassJsonMixin


@dataclass(slots=True)
class TimeEntry(DataClassJsonMixin):
    start: datetime
    end: datetime
    entry: str

    def __init__(self, start: datetime, end: datetime, entry: str):
        self.start = start
        self.end = end
        self.entry = entry


@dataclass(slots=True)
class TimeDayLog(DataClassJsonMixin):
    log_date: datetime
    file_name: str
    time_entries: list[TimeEntry]

    def __init__(self):
        today = datetime.today()
        self.log_date = datetime(
            year=today.year, month=today.month, day=today.day,
            hour=0, minute=0, second=0, microsecond=0
        )
        self.time_entries = []
        self.file_name = f"TimeTracking-{today.year}-{today.month}-{today.day}.log"
