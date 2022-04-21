from datetime import datetime, timedelta, time
from logging import Logger
from threading import Semaphore
from typing import Optional

from my_assistant.constants import LAST_ENTRY_FILE
from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.log_factory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui_facade import IUIFacadeService
from my_assistant.models.settings import Settings
from my_assistant.models.issues import Issue


class Assistant(IAssistant):
    time_tracking: ITimeTrackingService
    ui_service: IUIFacadeService
    task_file_service: ITaskFileService
    issue_service: IIssueService
    settings_service: ISettingsService
    log: Logger
    __lock__: Semaphore

    @property
    def time_interval(self) -> timedelta:
        return timedelta(
            hours=self.settings.interval_hours,
            minutes=self.settings.interval_minutes,
        )
    
    @property
    def last_entry_time(self) -> time:
        return self.task_file_service.get_last_entry_time(
            datetime.now()
        )
        
    @property
    def settings(self) -> Settings:
        return self.settings_service.get_settings()

    @property
    def issue_list(self) -> list[Issue]:
        return self.issue_service.get_issues_list()

    def __init__(
        self,
        time_tracking: ITimeTrackingService,
        ui_service: IUIFacadeService,
        task_file_service: ITaskFileService,
        issue_service: IIssueService,
        logging_factory: ILoggingFactory,
        settings_service: ISettingsService,
    ):
        self.log = logging_factory.get_logger("Assistant")
        self.settings_service = settings_service.get_settings()
        self.time_tracking = time_tracking
        self.ui_service = ui_service
        self.task_file_service = task_file_service
        self.issue_service = issue_service
        self.time_interval = timedelta(
            hours=self.settings.interval_hours,
            minutes=self.settings.interval_minutes,
        )
        self.ui_service.set_theme(self.settings.theme)
        self.__lock__ = Semaphore()

    
    def get_next(self, now: Optional[datetime] = None) -> datetime:
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

    @property
    def start_of_day(self) -> datetime:
        now = datetime.now()
        return datetime(
            now.year,
            now.month,
            now.day,
            self.settings.start_hour,
            self.settings.start_minute,
        )

    @property
    def end_of_day(self) -> datetime:
        now = datetime.now()
        return datetime(
            now.year,
            now.month,
            now.day,
            self.settings.end_hour,
            self.settings.end_minute,
        )

    def is_work_hour(self, date: datetime = None) -> bool:
        if date is None:
            date = datetime.now()
        return self.start_of_day <= date <= (self.end_of_day + self.time_interval)

    def is_work_time(self, time_of_day: datetime = None) -> bool:
        if time_of_day is None:
            time_of_day = datetime.now()
        return (
            self.settings.start_time < time_of_day < self.settings.end_time
            and time_of_day.weekday() in self.settings.days_of_week
        )

    def main_prompt(self, timestamp: datetime, manual_override: bool = False) -> datetime:
        self.log.debug("self.assistant.__lock__.acquire()")               
        self.__lock__.acquire()
        issue, comment = self.ui_service.record_time(timestamp, manual_override)
        self.log.info("Recording entry for %s", issue)
        self.log.debug("Issue: %s Comment: %s", issue, comment)
        try:
            if issue is not None:                
                message =  f"{issue} - {comment}"                
            else:
                message = "No comment for this time block"                
            try:
                self.task_file_service.create_tracking_entry(
                    timestamp, message, self.time_interval
                )
            except Exception as ex:
                self.log.exception(ex)
                self.ui_service.warning_prompt(
                    f"An unexpected error occurred writing an entry to the log file: {ex}"
                )                        
            return self.get_next(timestamp)
        finally:
            self.log.debug("self.assistant.__lock__.release()")
            self.__lock__.release()

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
            elif not self.is_work_day(now):
                self.log.info("%s is not a working day", now.strftime("%Y-%m-%d"))
            else:
                self.log.info(
                    "%s is not within working hours", now.strftime("%Y-%m-%d %H:%M:%S")
                )
