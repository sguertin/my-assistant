import base64
from datetime import datetime
import logging
import logging.config
from os import mkdir
from time import sleep

import PySimpleGUIQt as sg

from config import WORKING_DIR
from issues import get_issues_list
from jira import JiraResponse, JiraService, NEEDS_AUTH_CODE, FAILED_AUTH

from taskfile import create_tracking_entry, get_last_hour
from ui.credentials import credentials_prompt
from ui.time_tracking import record_time
from ui.warning import warning_prompt, warning_retry_prompt

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(name)-15s %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
)
sg.theme('DarkBlue3') 

log = logging.getLogger('TimeTracking')
log.setLevel(logging.INFO)

last_hour = get_last_hour()

def get_auth():
    user_name, password = credentials_prompt()
    encoding = base64.b64encode(f'{user_name}:{password}'.encode('utf-8'))    
    return encoding.decode()


if not WORKING_DIR.exists():
    log.info(f'Working directory not found at {WORKING_DIR}, creating...')
    mkdir(str(WORKING_DIR))


def is_workday(date: datetime) -> bool:
    return date.weekday() < 5

def is_workhour(date: datetime) -> bool:
    return date.hour > 8 and date.hour <= 17

now = datetime.now()

issues_list, issues_map = get_issues_list()

jira = JiraService(get_auth())

log.info('Initialization is complete, starting...')

def try_log_work(issue, comment) -> JiraResponse:
    retry = False
    response = jira.log_hours(issue['issue_num'], comment)
    if response.status_code != 201:
        log.warning(response.message)
        retry = warning_retry_prompt(response.message)
        if retry:
            if response.status_code in [NEEDS_AUTH_CODE, FAILED_AUTH]:
                jira.auth = get_auth()
            try_log_work(issue, comment)
    return response

def main_prompt(timestamp: datetime):
    issues_list, issues_map = get_issues_list()
    entry, comment = record_time(issues_list)
    if entry is not None:
        if entry not in issues_list: # Check if any new issue entries were added
            issues_list, issues_map = get_issues_list()
        try:
            issue = issues_map[entry]
            response = try_log_work(issue['issue_num'], comment)
            log.info(response)
        except KeyError:
            log.warning(f'Could not find an issue that matched {entry}')
        except Exception as ex:
            log.exception(ex)                
            warning_prompt(f'An unexpected error occurred posting log to Jira: {ex}')
        try:
            create_tracking_entry(timestamp, entry)
        except Exception as ex:
            log.exception(ex)
            warning_prompt(f'An unexpected error occurred writing an entry to the log file: {ex}')
    return datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour + 1, 0, 0)

if last_hour != 0:
    next = datetime(now.year, now.month, now.day, last_hour + 1, 0, 0)
else:
    next = datetime.now(now.year, now.month, now.day, 8, 0, 0)

while True:        
    now = datetime.now()
    if is_workday(now) and is_workhour(now) and now.hour >= next.hour:
        next = main_prompt(next)
        # if Prompt is left open and more than one hour passes
        # it will iterate through the hours that passed in between 
        while next.hour < datetime.now().hour and is_workhour(next):
            next = main_prompt(next)
    sleep(300)
