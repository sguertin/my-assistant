from datetime import datetime, timedelta, time
from logging import Logger
from typing import Optional

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.logfactory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.models.settings import Settings
from my_assistant.models.issues import Issue


class Assistant(IAssistant):
    time_tracking: ITimeTrackingService
    ui_provider: IUIFacadeService
    task_file_service: ITaskFileService
    issue_service: IIssueService
    settings: Settings
    log: Logger
    time_interval: timedelta
    last_entry_time: time

    @property
    def issue_list(self) -> list[Issue]:
        return self.issue_service.get_issues_list()

    def __init__(
        self,
        time_tracking: ITimeTrackingService,
        ui_provider: IUIFacadeService,
        task_file_service: ITaskFileService,
        issue_service: IIssueService,
        logging_factory: ILoggingFactory,
        settings_service: ISettingsService,
    ):
        self.log = logging_factory.get_logger("Assistant")
        self.settings = settings_service.get_settings()
        self.time_tracking = time_tracking
        self.ui_provider = ui_provider
        self.task_file_service = task_file_service
        self.issue_service = issue_service
        self.last_entry_time = self.task_file_service.get_last_entry_time(
            datetime.now()
        )
        self.time_interval = timedelta(
            hours=self.settings.interval_hours,
            minutes=self.settings.interval_minutes,
        )
        self.ui_provider.set_theme(self.settings.theme)

    def get_next(self, now: Optional[datetime] = None) -> datetime:
        """Calculates the next time an entry should be recorded

        Args:
            now (datetime, optional): The time of day to calculate from. Defaults to None.

        Returns:
            datetime: The next time an entry will need to be taken
        """
        if now is None:
            now = datetime.now()
        if self.last_entry_time:
            return (
                datetime(
                    now.year,
                    now.month,
                    now.day,
                    self.last_entry_time.hour,
                    self.last_entry_time.minute,
                )
                + self.time_interval
            )
        else:
            # No existing log file, assumes to start from the begining of the day
            return (
                datetime(
                    now.year,
                    now.month,
                    now.day,
                    self.settings.start_hour,
                    self.settings.start_minute,
                )
                + self.time_interval
            )

    @staticmethod
    def is_work_day(date: datetime) -> bool:
        return date.weekday() < 5

    def is_work_hour(self, date: datetime = None) -> bool:
        if date is None:
            date = datetime.now()
        start_of_day = datetime(
            date.year,
            date.month,
            date.day,
            self.settings.start_hour,
            self.settings.start_minute,
        )
        end_of_day = (
            datetime(
                date.year,
                date.month,
                date.day,
                self.settings.end_hour,
                self.settings.end_minute,
            )
            + self.time_interval
        )
        return start_of_day <= date <= end_of_day

    def is_work_time(self, time_of_day: datetime = None) -> bool:
        if time_of_day is None:
            time_of_day = datetime.now()
        return (
            self.settings.start_time < time_of_day < self.settings.end_time
            and time_of_day.weekday() in self.settings.days_of_week
        )

    def main_prompt(self, timestamp: datetime) -> datetime:
        issue, comment = self.ui_provider.record_time(timestamp)
        self.last_entry_time = timestamp.time()
        self.log.info("Recording entry for %s", issue)
        self.log.debug("Issue: %s Comment: %s", issue, comment)
        if issue is not None:
            try:
                self.time_tracking.try_log_work(
                    issue.issue_num, comment, self.time_interval
                )
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f"An unexpected error occurred posting log to Jira: {ex}"
                )
            try:
                self.task_file_service.create_tracking_entry(
                    timestamp, f"{issue} - {comment}", self.time_interval
                )
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f"An unexpected error occurred writing an entry to the log file: {ex}"
                )
        else:
            try:
                self.task_file_service.create_tracking_entry(
                    timestamp, "No entry for this time block", self.time_interval
                )
            except Exception as ex:
                self.log.exception(ex)
                self.ui_provider.warning_prompt(
                    f"An unexpected error occurred writing an entry to the log file: {ex}"
                )
        return self.get_next(timestamp)

    def run(self):
        next_timestamp = self.get_next()
        now = datetime.now()
        self.log.debug(
            "CHECK now="
            + now.strftime("%H:%M")
            + " >= next="
            + next_timestamp.strftime("%H:%M")
        )
        if now >= next_timestamp:
            if self.is_work_day(now) and self.is_work_hour(now):
                self.main_prompt(next_timestamp)
                # if Prompt is left open and more than one hour passes
                # it will iterate through the hours that passed in between
                while (
                    next_timestamp + self.time_interval
                ) < datetime.now() and self.is_work_hour(next_timestamp):
                    next_timestamp = self.main_prompt(next_timestamp)
