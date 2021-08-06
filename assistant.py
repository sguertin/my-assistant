from datetime import datetime, timedelta, time
import logging
from logging import Logger
import logging.config
from time import sleep

import PySimpleGUI as sg

from authentication import get_auth
from config import Settings, get_settings
from issues import Issue, get_issues_list
from jira import JiraResponse, JiraService, NEEDS_AUTH_CODE, FAILED_AUTH, MockJiraService
from taskfile import create_tracking_entry, get_last_entry_time
from ui.time_tracking import record_time
from ui.warning import warning_prompt, warning_retry_prompt


class Assistant:
    jira: JiraService
    time_interval: timedelta
    settings: Settings
    last_entry_time: datetime 
    log: Logger
    
    @staticmethod
    def is_workday(date: datetime) -> bool:
        return date.weekday() < 5
    
    def is_workhour(self, date: datetime) -> bool:
        start_of_day = datetime(date.year, date.month, date.day, self.settings.start_hour, self.settings.start_minute)
        end_of_day = datetime(date.year, date.month, date.day, self.settings.end_hour, self.settings.end_minute) + self.time_interval
        return date >= start_of_day and date <= end_of_day
    
    def __init__(self):        
        self.settings = get_settings()
        if self.settings.enable_jira:
            self.jira = JiraService(get_auth())
        else:
            self.jira = MockJiraService('')
        
        self.last_entry_time = get_last_entry_time(datetime.now())
        self.time_interval = timedelta(
            hours=self.settings.interval_hours, 
            minutes=self.settings.interval_minutes,
        )
        self.log = logging.getLogger('my-assistant.assistant')
        self.log.setLevel(logging.INFO)         
        self.log.info('Assistant class initialization is complete')

    def try_log_work(self, issue: Issue, comment: str) -> JiraResponse:
        response = self.jira.log_hours(issue, comment, self.time_interval)
        if response.status_code != 201:
            self.log.warning(response.message)
            retry = warning_retry_prompt(response.message)
            if retry:
                if response.status_code in [NEEDS_AUTH_CODE, FAILED_AUTH]:
                    self.jira.auth = get_auth()
                return self.try_log_work(issue, comment)
        return response

    def main_prompt(self, timestamp: datetime):
        issues_list = get_issues_list()
        issue, comment = record_time(issues_list, timestamp)
        self.last_entry_time = timestamp.time()
        
        if issue is not None:
            if issue not in issues_list: # Check if any new issue entries were added
                issues_list = get_issues_list()
            try:
                response = self.try_log_work(issue.issue_num, comment)
                self.log.debug(response)
            except Exception as ex:
                self.log.exception(ex)                
                warning_prompt(f'An unexpected error occurred posting log to Jira: {ex}')
            try:
                create_tracking_entry(timestamp, f'{issue} - {comment}', self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                warning_prompt(f'An unexpected error occurred writing an entry to the log file: {ex}')
        else:
            try:
                create_tracking_entry(timestamp, 'No entry for this timeblock', self.time_interval)
            except Exception as ex:
                self.log.exception(ex)
                warning_prompt(f'An unexpected error occurred writing an entry to the log file: {ex}')
    
    def get_next(self) -> datetime:
        now = datetime.now()
        if self.last_entry_time:
            return datetime(now.year, now.month, now.day, self.last_entry_time.hour, self.last_entry_time.minute) + self.time_interval
        else: 
            # No existing log file, assumes to start from the begining of the day
            return datetime(now.year, now.month, now.day, self.settings.start_hour, self.settings.start_minute) + self.time_interval
            
    def run(self):
        while True:
            next = self.get_next()
            now = datetime.now()
            self.settings = get_settings()
            self.log.debug('CHECK now=' + now.strftime('%H:%M') + ' >= next=' + next.strftime('%H:%M'))
            if now >= next:
                self.jira.base_url = self.settings.base_url
                if self.is_workday(now) and self.is_workhour(now):            
                    sg.theme(self.settings.theme)            
                    self.main_prompt(next, self.time_interval)                    
                    # if Prompt is left open and more than one hour passes
                    # it will iterate through the hours that passed in between 
                    while (next + self.time_interval) < datetime.now() and self.is_workhour(next):
                        self.main_prompt(next)
                        next = next + self.time_interval                
            sleep(300)