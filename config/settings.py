from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from os import getenv, mkdir
from pathlib import Path

from dataclasses_json import dataclass_json, LetterCase

log = logging.getLogger('TimeTracking.config')
log.setLevel(logging.INFO)

WORKING_DIR: Path = Path(getenv('USERPROFILE'), 'TimeTracking')
ISSUES_LIST: Path = Path(WORKING_DIR, 'issues.json')
DELETED_ISSUES_LIST: Path = Path(WORKING_DIR, 'deletedIssues.json')
SETTINGS_FILE: Path = Path(WORKING_DIR, 'settings.json')
MINUTE_RANGE: range = range(60)
HOUR_RANGE: range = range(24)
DAY: timedelta = datetime(2000, 10, 20) - datetime(2000, 10, 19)

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

    def validate(self) -> list[str]:
        error_list = []
        if self.start_hour not in HOUR_RANGE:
            error_list.append(f'Start Hour {self.start_hour} is not between 0 and 23')
        if self.end_hour not in HOUR_RANGE:
            error_list.append(f'End Hour {self.end_hour} is not between 0 and 23')
        if self.start_minute not in MINUTE_RANGE:
            error_list.append(f'Start Minute {self.start_minute} is not between 0 and 59')
        if self.end_minute not in MINUTE_RANGE:
            error_list.append(f'End Minute {self.end_minute} is not between 0 and 59')

        now = datetime.now()        
        start_time = datetime(now.year, now.day, now.month, self.start_hour, self.start_minute)
        end_time = datetime(now.year, now.day, now.month, self.end_hour, self.end_minute)
        if self.start_hour > self.end_hour:
            end_time = end_time + DAY
        interval_time = datetime(now.year, now.day, now.month, self.interval_hours, self.interval_minutes) - datetime(now.year, now.month, now.day, 0, 0, 0)
        total_workday = start_time - end_time
        if total_workday < interval_time:
            error_list.append(f'Entire workday [{self.start_hour}:{self.start_minute}] - [{self.end_hour}:{self.end_minute}] '+
                            f'is less than time recording interval: [{self.interval_hours}:{self.interval_minutes}]')
        return error_list
    
    def save(self) -> None:
        with open(SETTINGS_FILE, 'w') as f:
            f.write(self.to_json())

def restore_defaults() -> None:
    Settings().save()
    

def get_settings() -> Settings:
    if not SETTINGS_FILE.exists():
        settings = Settings()
        settings.save()
        return settings
    else:
        with open(SETTINGS_FILE, 'r') as f:
            return Settings.from_json(f.read())
