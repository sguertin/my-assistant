from datetime import datetime, timedelta
import logging
from logging import Logger
import logging.config

import PySimpleGUI as sg

from services.issues import get_issues_list
from services.taskfile import create_tracking_entry, get_last_entry_time

from interfaces.time_tracking import ITimeTrackingService
from interfaces.ui import IUIProvider
from models.settings import Settings


class Assistant:
    time_tracking: ITimeTrackingService
    time_interval: timedelta
    settings: Settings
    last_entry_time: datetime
    log: Logger

    @staticmethod
    def is_workday(date: datetime) -> bool:
        """Checks if the date provided is a workday

        Args:
            date (datetime): The date to check for being a workday

        Returns:
            bool: True if the date is a workday
        """
        return date.weekday() < 5

    def is_work_time(self, time_of_day: datetime = None) -> bool:
        """Determines if the given time (now by default) is within working hours

        Args:
            time_of_day (datetime, optional): The time of day that needs to be determined if it's during work hours. Defaults to None.

        Returns:
            bool: True if time_of_day is within work hours
        """
        if time_of_day is None:
            time_of_day = datetime.now()
        return self.settings.start_time < time_of_day < self.settings.end_time and time_of_day.weekday() in self.settings.days_of_week

    def is_workhour(self, date: datetime) -> bool:
        start_of_day = datetime(date.year, date.month, date.day,
                                self.settings.start_hour, self.settings.start_minute)
        end_of_day = datetime(date.year, date.month, date.day,
                              self.settings.end_hour, self.settings.end_minute) + self.time_interval
        return date >= start_of_day and date <= end_of_day

    def __init__(self, time_tracking: ITimeTrackingService, ui_provider: IUIProvider, settings: Settings):
        self.settings = settings
        self.time_tracking = time_tracking
        self.ui_provider = ui_provider
        self.issues_list = get_issues_list()
        self.last_entry_time = get_last_entry_time(datetime.now())
        self.time_interval = timedelta(
            hours=self.settings.interval_hours,
            minutes=self.settings.interval_minutes,
        )
        self.log = logging.getLogger('Assistant')
        self.log.setLevel(self.settings.log_level)
        self.log.info('Assistant class initialization is complete')
        sg.theme(settings.theme)

    def run(self):
        next_timestamp = self.get_next()
        now = datetime.now()
        self.log.debug('CHECK now=' + now.strftime('%H:%M') +
                       ' >= next=' + next_timestamp.strftime('%H:%M'))
        if now >= next_timestamp:
            if self.is_workday(now) and self.is_workhour(now):
                self.main_prompt(next_timestamp, self.time_interval)
                # if Prompt is left open and more than one hour passes
                # it will iterate through the hours that passed in between
                while (next_timestamp + self.time_interval) < datetime.now() and self.is_workhour(next_timestamp):
                    next_timestamp = self.main_prompt(next_timestamp)

    def main_prompt(self, timestamp: datetime) -> datetime:
        issue, comment = self.ui_provider.record_time(timestamp)
        self.last_entry_time = timestamp.time()

        if issue is not None:
            if issue not in self.issues_list:  # Check if any new issue entries were added
                self.issues_list = get_issues_list()
            try:
                self.time_tracking.try_log_work(
                    issue.issue_num, comment, self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f'An unexpected error occurred posting log to Jira: {ex}')
            try:
                create_tracking_entry(
                    timestamp, f'{issue} - {comment}', self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f'An unexpected error occurred writing an entry to the log file: {ex}')
        else:
            try:
                create_tracking_entry(
                    timestamp, 'No entry for this timeblock', self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f'An unexpected error occurred writing an entry to the log file: {ex}')
        return self.get_next(timestamp)

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
