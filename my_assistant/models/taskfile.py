from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(slots=True)
class TimeEntry:
    start: datetime
    end: datetime
    entry: str

    def __init__(self, start: datetime, end: datetime, entry: str):
        self.start = start
        self.end = end
        self.entry = entry


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(slots=True)
class TimeDayLog:
    log_date: datetime
    file_name: str
    time_entries: list[TimeEntry]

    def __init__(self, log_date: datetime = None, file_name: str = None, time_entries: list[TimeEntry] = None):
        if log_date is None:
            log_date = datetime.today()
        if file_name is None:
            file_name = f"TimeTracking-{log_date.year}-{log_date.month}-{log_date.day}.log"
        if time_entries is None:
            time_entries = []
        self.log_date = log_date
        self.time_entries = time_entries
        self.file_name = file_name
