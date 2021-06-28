from datetime import datetime
import logging
import logging.config
from time import sleep

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(name)-15s %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
)
import PySimpleGUI as sg

from authentication import get_auth
from issues import get_issues_list
from jira import JiraResponse, JiraService, NEEDS_AUTH_CODE, FAILED_AUTH, MockJiraService
from taskfile import create_tracking_entry, get_last_hour
from ui.time_tracking import record_time
from ui.warning import warning_prompt, warning_retry_prompt

sg.theme('DarkBlue3') 
log = logging.getLogger('TimeTracking')
log.setLevel(logging.INFO)

last_hour = get_last_hour()
def is_workday(date: datetime) -> bool:
    return date.weekday() < 5

def is_workhour(date: datetime) -> bool:
    return date.hour > 8 and date.hour <= 17

now = datetime.now()

issues_list, issues_map = get_issues_list()

jira = MockJiraService(get_auth())

log.info('Initialization is complete, starting...')

def try_log_work(issue, comment) -> JiraResponse:
    retry = False
    response = jira.log_hours(issue, comment)
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
    entry, comment = record_time(issues_list, timestamp)
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
    # No existing log file, assumes to start from the begining of the day
    next = datetime(now.year, now.month, now.day, 8, 0, 0)

while True:        
    now = datetime.now()
    if is_workday(now) and is_workhour(now) and now.hour >= next.hour:
        next = main_prompt(next)
        # if Prompt is left open and more than one hour passes
        # it will iterate through the hours that passed in between 
        while next.hour < datetime.now().hour and is_workhour(next):
            next = main_prompt(next)
    sleep(300)
