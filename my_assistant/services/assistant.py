from datetime import datetime, timedelta
from functools import lru_cache
import logging
from logging import Logger
from my_assistant.constants import HOUR_RANGE, MINUTE_RANGE, LOGGING_LEVELS, DAYS_OF_WEEK

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.models.settings import Settings


@lru_cache(maxsize=1)
def start_time(settings: Settings, now: datetime) -> datetime:
    """Get the starting work time for the current day

    Returns:
        datetime: date/time of the start of work day
    """
    if settings.start_hour > settings.end_hour and now.hour <= settings.end_hour and now.minute <= settings.end_minute:
        return datetime(now.year, now.day, now.month, settings.start_hour, settings.start_minute, 0) - timedelta(days=1)
    return datetime(now.year, now.day, now.month,
                    settings.start_hour, settings.start_minute, 0)


@lru_cache(maxsize=1)
def end_time(settings: Settings, now: datetime) -> datetime:
    """Get the ending work time for the current day

    Returns:
        datetime: date/time of the end of work day
    """
    if settings.start_hour > settings.end_hour and now.hour >= settings.end_hour:
        return datetime(now.year, now.day, now.month, settings.end_hour, settings.end_minute, 0) + timedelta(days=1)
    return datetime(now.year, now.day, now.month, settings.end_hour, settings.end_minute, 0)


@lru_cache(maxsize=1)
def work_day(start_time: datetime, end_time: datetime) -> str:
    """The duration of a workday

    Returns:
        timedelta: time between start_time and end_time
    """

    return end_time - start_time


@lru_cache(maxsize=1)
def work_day_text(work_day: timedelta) -> str:
    """The duration of a workday

    Returns:
        timedelta: time between start_time and end_time
    """
    seconds = work_day.seconds
    hours = int(seconds / 360)
    minutes = int((seconds % 360) / 60)
    return f'{hours}h {minutes}m'


@lru_cache(maxsize=1)
def validate_settings(settings: Settings, work_day: timedelta, work_day_text: str) -> list[str]:
    """Validates if the settings provided are valid

    Returns:
        list[str]: List of errors found during validation process
    """
    error_list = []
    start_hour, start_minute, end_hour, end_minute, interval_hours, interval_minutes = (
        settings.start_hour,
        settings.start_minute,
        settings.end_hour,
        settings.end_minute,
        settings.interval_hours,
        settings.interval_minutes)

    if start_hour not in HOUR_RANGE:
        error_list.append(
            f'Start Hour {start_hour:02d} is not between 00 and 23')
    if end_hour not in HOUR_RANGE:
        error_list.append(
            f'End Hour {end_hour:02d} is not between 00 and 23')
    if start_minute not in MINUTE_RANGE:
        error_list.append(
            f'Start Minute {start_minute:02d} is not between 00 and 59')
    if end_minute not in MINUTE_RANGE:
        error_list.append(
            f'End Minute {end_minute:02d} is not between 00 and 59')
    if interval_hours == 0 and interval_minutes == 0:
        error_list.append(f'No time interval specified')
    if work_day < settings.time_interval:

        error_list.append(f'Entire workday [{start_hour:02d}:{start_minute:02d}] - [{end_hour:02d}:{end_minute:02d}] = {work_day_text}' +
                          f'is less than time recording interval: [{interval_hours}:{interval_minutes}]')
    return error_list


class Assistant(IAssistant):
    task_service: ITaskFileService
    time_tracking: ITimeTrackingService
    ui_provider: IUIProvider

    time_interval: timedelta
    settings: Settings
    last_entry_time: datetime
    log: Logger

    def __init__(self,
                 time_tracking: ITimeTrackingService,
                 ui_provider: IUIProvider,
                 task_service: ITaskFileService,
                 issue_service: IIssueService,
                 settings: Settings):
        """Assistant is the orchestrator of the component services, keeping track of when to record time

        Args:
            time_tracking (ITimeTrackingService): Service that handles communication with time tracking 
            ui_provider (IUIProvider): Service that provides UI Controls
            task_service (ITaskFileService): Service that handles the task log
            issue_service (IIssueService): Service that handles the list of active and inactive issues
            settings (Settings): The application settings
        """
        self.settings = settings
        self.task_service = task_service
        self.time_tracking = time_tracking
        self.ui_provider = ui_provider
        self.issue_service = issue_service
        self.issues_list = issue_service.get_issues_list()
        self.last_entry_time = task_service.get_last_entry_time(datetime.now())
        self.time_interval = settings.time_interval
        self.log = logging.getLogger('Assistant')
        self.log.setLevel(settings.log_level)
        errors = self.settings_are_valid()
        if errors:
            error_message = f'Invalid settings provided!\n' + '\n'.join(errors)
            self.ui_provider.warning_prompt(error_message)
            self.log.error(error_message)

            raise Exception(error_message)
        self.log.info('Assistant class initialization is complete')

    def run(self):
        next_timestamp = self.get_next()
        now = datetime.now()
        self.log.debug('CHECK now=' + now.strftime('%H:%M') +
                       ' >= next=' + next_timestamp.strftime('%H:%M'))
        if now >= next_timestamp:
            if self.is_work_time(now):
                next_timestamp = self.main_prompt(next_timestamp)
                # if Prompt is left open and more than time interval passes
                # it will iterate through the intervals that passed in between
                while next_timestamp < datetime.now() and self.is_work_time(next_timestamp):
                    next_timestamp = self.main_prompt(next_timestamp)
                if not self.is_work_time(next_timestamp):
                    self.ui_provider.warning_prompt(
                        'Hooray, the day\'s is over!')

    def main_prompt(self, timestamp: datetime) -> datetime:
        issue, comment = self.ui_provider.record_time(
            timestamp, lambda: self.issue_service.manage_issues)
        self.last_entry_time = timestamp.time()

        if issue is not None:
            if issue not in self.issues_list:  # Check if any new issue entries were added
                self.issues_list = self.issue_service.get_issues_list()
            try:
                self.time_tracking.try_log_work(
                    issue.issue_num, comment, self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f'An unexpected error occurred posting log to Jira: {ex}')
            try:
                self.task_service.create_tracking_entry(
                    timestamp, f'{issue} - {comment}', self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f'An unexpected error occurred writing an entry to the log file: {ex}')
        else:
            try:
                self.task_service.create_tracking_entry(
                    timestamp, 'No entry for this timeblock', self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f'An unexpected error occurred writing an entry to the log file: {ex}')
        return self.get_next(timestamp)

    @property
    def start_time(self):
        return start_time(self.settings, datetime.now())

    @property
    def end_time(self):
        return end_time(self.settings, datetime.now())

    @property
    def work_day(self) -> timedelta:
        """The duration of a workday

        Returns:
            timedelta: time between start_time and end_time
        """
        return work_day(self.end_time, self.start_time)

    @property
    def work_day_text(self) -> str:
        """Get text version of work_day duration

        Returns:
            str: text representation of time
        """
        return work_day_text(self.work_day)

    def settings_are_valid(self) -> list[str]:
        return validate_settings(self.settings, self.work_day, self.work_day_text)

    def is_work_time(self, time_of_day: datetime = None) -> bool:
        """Determines if the given time (now by default) is within working hours

        Args:
            time_of_day (datetime, optional): The time of day that needs to be determined if it's during work hours. Defaults to None.

        Returns:
            bool: True if time_of_day is within work hours
        """
        if time_of_day is None:
            time_of_day = datetime.now()
        return self.start_time < time_of_day < self.end_time \
            and time_of_day.weekday() in self.settings.days_of_week

    def get_next(self, now: datetime = None) -> datetime:
        """Calculates the next time an entry should be recorded

        Args:
            now (datetime, optional): The time of day to calculate from. Defaults to None.

        Returns:
            datetime: The next time an entry will need to be taken
        """
        if now is None:
            now = datetime.now()
        if self.last_entry_time:
            return datetime(now.year, now.month, now.day, self.last_entry_time.hour, self.last_entry_time.minute) + self.time_interval
        else:
            # No existing log file, assumes to start from the begining of the day
            return datetime(now.year, now.month, now.day, self.settings.start_hour, self.settings.start_minute) + self.time_interval
