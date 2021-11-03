from datetime import datetime, timedelta, time
from logging import Logger
import logging
from pathlib import Path


from my_assistant.constants import WORKING_DIR
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.models.settings import Settings
from my_assistant.models.taskfile import TimeDayLog, TimeEntry


class TaskFileService(ITaskFileService):
    """Service that handles reading and writing from the file log of time entries"""
    log: Logger

    def __init__(self, settings: Settings):
        """Initialize the Task File Service

        Args:
            settings (Settings): The application settings
        """
        self.log = logging.getLogger('TaskFileService')
        self.log.setLevel(settings.log_level)

    def create_tracking_entry(self, timestamp: datetime, entry: str, time_interval: timedelta):
        task_log: TimeDayLog = self.get_time_log(timestamp)

        task_log.time_entries.append(
            TimeEntry((timestamp - time_interval), timestamp, entry))
        task_log.save()

    def get_last_entry_time(self, timestamp: datetime) -> time:
        task_log = self.get_time_log(timestamp)
        if len(task_log.time_entries) > 0:
            return task_log.time_entries[-1].end_time.time()
        return None

    def get_time_log_path(self, timestamp: datetime) -> Path:
        return Path(WORKING_DIR, f'TimeTracking-{timestamp.year}-{timestamp.month}-{timestamp.day}.log')

    def get_time_log(self, timestamp: datetime) -> TimeDayLog:
        task_file = self.get_time_log_path(timestamp)

        if not task_file.exists():
            self.log.info(
                f'No log file found for {timestamp.month}/{timestamp.day}/{timestamp.year}, creating new log file')
            task_log = TimeDayLog(timestamp)
        else:
            try:
                self.log.info(
                    f'Existing task file found at: {self.get_time_log_path(timestamp)}')
                with open(task_file, 'r') as f:
                    contents = f.read()
                    task_log = TimeDayLog.from_json(contents)
            except Exception as ex:
                self.log.error(
                    f'get_time_log: An error occurred loading the log file: {ex}')
                self.log.exception(ex)
                self.log.info('Creating new log file...')
                task_log = TimeDayLog(timestamp)
                task_log.save()
        return task_log
