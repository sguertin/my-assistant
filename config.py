import logging
from os import getenv, mkdir
from pathlib import Path
from configparser import ConfigParser

log = logging.getLogger('TimeTracking.config')
log.setLevel(logging.INFO)

WORKING_DIR: Path = Path(getenv('USERPROFILE'), 'TimeTracking')
ISSUES_LIST: Path = Path(WORKING_DIR, 'issues.json')
DELETED_ISSUES_LIST: Path = Path(WORKING_DIR, 'deletedIssues.json')
SETTINGS_FILE: Path = Path(WORKING_DIR, 'settings.ini')

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

def create_default_config():
    default_config = ConfigParser()
    default_config.add_section('AppSettings')
    default_config.set('AppSettings', 'theme', 'DarkBlue3')
    default_config.add_section('JiraSettings')
    default_config.set('JiraSettings', 'base_url', 'https://jira.housingcenter.com')
    with open(SETTINGS_FILE, 'w') as f:
        default_config.write(f)
    return default_config

if SETTINGS_FILE.exists():
    configuration = ConfigParser()
    configuration.read(str(SETTINGS_FILE))   
else:
    configuration = create_default_config()

CONFIG: ConfigParser = configuration
JIRA_URL: str = configuration.get('JiraSettings', 'base_url', fallback='https://jira.housingcenter.com')
THEME: str = configuration.get('AppSettings', 'theme', fallback='DarkBlue3')
