from datetime import datetime, timedelta, date, time
from pathlib import Path

from ..constants import WORKING_DIR
from ..models.taskfile import TimeDayLog, TimeEntry


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

    task_log.time_entries.append(
        TimeEntry(timestamp - time_interval, timestamp, entry))
    with open(get_time_log_path(timestamp), 'w') as f:
        f.write(task_log.to_json())


def get_last_entry_time(timestamp: datetime) -> time:
    task_log = get_time_log(timestamp)
    if len(task_log.time_entries) > 0:
        return task_log.time_entries[-1].end_time
    return None
