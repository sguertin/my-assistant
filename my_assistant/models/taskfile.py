from dataclasses import dataclass
from datetime import datetime, time

from dataclasses_json import DataClassJsonMixin


@dataclass
class TimeEntry(DataClassJsonMixin):
    start_time: time
    end_time: time
    entry: str

    def __init__(self, start_time: datetime, end_time: datetime, entry: str):
        self.start_time = start_time.time()
        self.end_time = end_time.time()
        self.entry = entry


@dataclass
class TimeDayLog(DataClassJsonMixin):
    log_date: datetime
    file_name: str
    time_entries: list[TimeEntry]

    def __init__(self):
        today = datetime.today()
        self.log_date = today
        self.time_entries = []
        self.file_name = f"TimeTracking-{today.year}-{today.month}-{today.day}.log"
