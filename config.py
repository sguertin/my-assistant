from configparser import ConfigParser
from dataclasses import dataclass
from datetime import timedelta
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
    base_url: str = 'https://jira.housingcenter.com'    
    start_hour: int = 8
    start_minute: int = 0
    end_hour: int = 17
    end_minute: int = 0
    interval_hours: int = 1
    interval_minutes: int = 0
    enable_jira: bool = True
    
    def save(self):
        with open(SETTINGS_FILE, 'w') as f:
            f.write(self.to_json())

def get_settings() -> Settings:
    if not SETTINGS_FILE.exists():
        settings = Settings()
        settings.save()
        return settings
    else:
        with open(SETTINGS_FILE, 'r') as f:
            return Settings.from_json(f.read())
