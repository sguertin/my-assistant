from datetime import datetime, timedelta, time
from json import JSONDecodeError
from logging import Logger
from pathlib import Path
from typing import Optional

from my_assistant.constants import WORKING_DIR
from my_assistant.factories.interfaces.log_factory import ILoggingFactory
from my_assistant.services.interfaces.taskfile import ITaskFileService
from my_assistant.models.taskfile import TimeDayLog, TimeEntry


class TaskFileService(ITaskFileService):
    log: Logger

    def __init__(self, log_factory: ILoggingFactory):
        self.log = log_factory.get_logger("TaskFileService")

    @staticmethod
    def get_time_log_path(timestamp: datetime) -> Path:
        return Path(
            WORKING_DIR,
            f"TimeTracking-{timestamp.year}-{timestamp.month}-{timestamp.day}.log",
        )

    def get_time_log(self, timestamp: datetime) -> TimeDayLog:
        try:
            task_file = self.get_time_log_path(timestamp)
            if not task_file.exists():
                task_log = TimeDayLog()
            else:
                with open(task_file, "r") as f:
                    task_log = TimeDayLog.from_json(f.read())
        except JSONDecodeError as ex:
            self.log.exception(ex)
            task_log = TimeDayLog()
        return task_log

    def create_tracking_entry(
        self, timestamp: datetime, entry: str, time_interval: timedelta
    ):
        task_log: TimeDayLog = self.get_time_log(timestamp)

        task_log.time_entries.append(
            TimeEntry(timestamp - time_interval, timestamp, entry)
        )
        try:
            with open(self.get_time_log_path(timestamp), "w") as f:
                f.write(task_log.to_json(indent=4))
        except OSError as ex:
            self.log.exception(ex)
            raise

    def get_last_entry_time(self, timestamp: datetime) -> Optional[time]:
        task_log = self.get_time_log(timestamp)
        if len(task_log.time_entries) > 0:
            return task_log.time_entries[-1].end
        return None
