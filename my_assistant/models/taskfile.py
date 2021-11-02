from dataclasses import dataclass, field
from datetime import datetime, date, time

from dataclasses_json import dataclass_json, LetterCase

from my_assistant.constants import WORKING_DIR


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimeEntry:
    start_time: datetime
    end_time: datetime
    entry: str

    def __init__(self, start_time: datetime, end_time: datetime, entry: str):
        self.start_time = start_time
        self.end_time = end_time
        self.entry = entry


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimeDayLog:
    log_date: datetime
    file_name: str
    time_entries: list[TimeEntry]

    def __init__(self, log_date: datetime = None, file_name: str = None, time_entries: list[TimeEntry] = None):
        if log_date is None:
            log_date = datetime.now()
        self.log_date = datetime(
            log_date.year, log_date.month, log_date.day, 0, 0, 0)
        if file_name is None:
            file_name = f'TimeTracking-{log_date.year}-{log_date.month}-{log_date.day}.log'
        self.file_name = file_name
        if time_entries is None:
            time_entries = []
        self.time_entries = time_entries

    def save(self) -> None:
        with open(WORKING_DIR / self.file_name, 'w') as f:
            f.write(self.to_json())
