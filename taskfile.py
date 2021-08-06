from dataclasses import dataclass, field
from datetime import datetime, timedelta, date, time
import logging
from pathlib import Path

from dataclasses_json import dataclass_json, LetterCase

from config import get_settings, WORKING_DIR

log = logging.getLogger('TimeTracking')
log.setLevel(logging.INFO)

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


def get_time_log_path(timestamp: datetime) -> Path:
    return Path(WORKING_DIR, f'TimeTracking-{timestamp.year}-{timestamp.month}-{timestamp.day}.log')

def get_time_log(timestamp: datetime) -> TimeDayLog:
    task_file = get_time_log_path(timestamp)
    if not task_file.exists():
        task_log = TimeDayLog()
    else:
        with open(task_file, 'r') as f:
            task_log = TimeDayLog.from_json(f.read())
    return task_log        

def create_tracking_entry(timestamp: datetime, entry: str, time_interval: timedelta):    
    task_log: TimeDayLog = get_time_log(timestamp)
    
    task_log.time_entries.append(TimeEntry(timestamp - time_interval, timestamp, entry))
    with open(get_time_log_path(timestamp), 'w') as f:
        f.write(task_log.to_json())

def get_last_entry_time(timestamp: datetime) -> time:
    task_log = get_time_log(timestamp)
    if len(task_log.time_entries) > 0:
        return task_log.time_entries[-1].end_time # 
    return None

