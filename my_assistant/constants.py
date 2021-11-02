import logging
from os import getenv
from pathlib import Path

WORKING_DIR: Path = Path(getenv('USERPROFILE'), 'TimeTracking')
ISSUES_LIST: Path = Path(WORKING_DIR, 'issues.json')
DELETED_ISSUES_LIST: Path = Path(WORKING_DIR, 'deletedIssues.json')
SETTINGS_FILE: Path = Path(WORKING_DIR, 'settings.json')

HOUR_RANGE: range = range(24)
MINUTE_RANGE: range = range(60)

DAYS_OF_WEEK = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}
LOGGING_LEVELS = {
    'Critical': logging.CRITICAL,
    'Error': logging.ERROR,
    'Warning': logging.WARNING,
    'Info': logging.INFO,
    'Debug': logging.DEBUG,
}