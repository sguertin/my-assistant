import logging
from os import getenv, mkdir
from pathlib import Path
from configparser import ConfigParser

log = logging.getLogger('config.py')
log.setLevel(logging.INFO)

WORKING_DIR = Path(getenv('USERPROFILE'), 'TimeTracking')
ISSUES_LIST = Path(WORKING_DIR, 'issues.json')
SETTINGS_FILE = Path(WORKING_DIR, 'settings.ini')

if not WORKING_DIR.exists():
    log.info(f'Working directory not found at {WORKING_DIR}, creating...')
    mkdir(str(WORKING_DIR))

def create_default_config():
    default_config = ConfigParser()
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

JIRA_URL = configuration.get('JiraSettings', 'base_url')
