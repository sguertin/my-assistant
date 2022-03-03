from dataclasses import dataclass
from datetime import datetime, date, time

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimeEntry:
    start_time: time
    end_time: time
    entry: str

    def __init__(self, start_time: datetime, end_time: datetime, entry: str):
        self.start_time = start_time.time()
        self.end_time = end_time.time()
        self.entry = entry


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimeDayLog:
    log_date: date
    file_name: str
    time_entries: list[TimeEntry]

    def __init__(self):
        today = date.today()
        self.log_date = today
        self.time_entries = []
        self.file_name = f'TimeTracking-{today.year}-{today.month}-{today.day}.log'