from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from os import getenv, mkdir
from pathlib import Path

from dataclasses_json import dataclass_json, LetterCase

log = logging.getLogger('Settings')
log.setLevel(logging.INFO)

LOGGING_LEVELS = {
    'Critical': logging.CRITICAL,
    'Error': logging.ERROR,
    'Warning': logging.WARNING,
    'Info': logging.INFO,
    'Debug': logging.DEBUG,
}
DAYS_OF_WEEK = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}
WORKING_DIR: Path = Path(getenv('USERPROFILE'), 'TimeTracking')
ISSUES_LIST: Path = Path(WORKING_DIR, 'issues.json')
DELETED_ISSUES_LIST: Path = Path(WORKING_DIR, 'deletedIssues.json')
SETTINGS_FILE: Path = Path(WORKING_DIR, 'settings.json')
MINUTE_RANGE: range = range(60)
HOUR_RANGE: range = range(24)


if not WORKING_DIR.exists():
    log.info(f'Working directory not found at {WORKING_DIR}, creating...')
    mkdir(str(WORKING_DIR))

if not ISSUES_LIST.exists():
    log.info(f'Issues list not found, creating new list')
    with open(ISSUES_LIST, 'a') as f:
        f.write('[]')

if not DELETED_ISSUES_LIST.exists():
    with open(DELETED_ISSUES_LIST, 'a') as f:
        f.write('[]')


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Settings:
    theme: str = 'DarkBlue3'
    base_url: str = ''
    start_hour: int = 8
    start_minute: int = 0
    end_hour: int = 17
    end_minute: int = 0
    interval_hours: int = 1
    interval_minutes: int = 0
    enable_jira: bool = True
    log_level: int = logging.INFO
    days_of_week: list[int] = [0, 1, 2, 3, 4]
    
    @property
    def time_interval(self) -> timedelta:
        return timedelta(
            hours=self.interval_hours, 
            minutes=self.interval_minutes
        )    

    @property
    def start_time(self) -> datetime:
        now = datetime.now()
        if self.start_hour > self.end_hour and now.hour <= self.end_hour:
            return datetime(now.year, now.day, now.month, self.start_hour, self.start_minute, 0) - timedelta(days=1)    
        return datetime(now.year, now.day, now.month,
                        self.start_hour, self.start_minute, 0)

    @property
    def end_time(self) -> datetime:
        now = datetime.now()
        if self.start_hour > self.end_hour and now.hour <= self.end_hour:
            return datetime(now.year, now.day, now.month, self.end_hour, self.end_minute, 0)
        return datetime(now.year, now.day, now.month, self.end_hour, self.end_minute, 0) + timedelta(days=1)    
    
    @property
    def work_day(self) -> timedelta:
        return self.end_time - self.start_time
    
    def validate(self) -> list[str]:
        error_list = []
        if self.start_hour not in HOUR_RANGE:
            error_list.append(
                f'Start Hour {self.start_hour:02d} is not between 00 and 23')
        if self.end_hour not in HOUR_RANGE:
            error_list.append(
                f'End Hour {self.end_hour:02d} is not between 00 and 23')
        if self.start_minute not in MINUTE_RANGE:
            error_list.append(
                f'Start Minute {self.start_minute:02d} is not between 00 and 59')
        if self.end_minute not in MINUTE_RANGE:
            error_list.append(
                f'End Minute {self.end_minute:02d} is not between 00 and 59')
        if self.interval_hours == 0 and self.interval_minutes == 0:
            error_list.append(f'No time interval specified')
        if self.work_day < self.time_interval:
            error_list.append(f'Entire workday [{self.start_hour:02d}:{self.start_minute:02d}] - [{self.end_hour:02d}:{self.end_minute:02d}] = {self.work_day.hours}h {self.work_day.minutes}' +
                              f'is less than time recording interval: [{self.interval_hours}:{self.interval_minutes}]')
        return error_list

    def save(self) -> None:
        with open(SETTINGS_FILE, 'w') as f:
            f.write(self.to_json())


def restore_defaults() -> None:
    Settings().save()


def get_settings() -> Settings:
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r') as f:
            settings = clean_settings(Settings.from_json(f.read()))            
            return settings
    else:
        settings = Settings()
        settings.save()
        return settings
    


def clean_settings(self: Settings) -> Settings:
    start_hour = abs(self.start_hour)
    start_minute = abs(self.start_minute)
    end_hour = abs(self.end_hour)
    end_minute = abs(self.end_minute)
    interval_hours = abs(self.interval_hours)
    interval_minutes = abs(self.interval_minutes)
    return Settings(self.theme, self.base_url, start_hour, start_minute, end_hour, end_minute,
                    interval_hours, interval_minutes, self.enable_jira, self.log_level)
