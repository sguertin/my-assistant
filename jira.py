import base64
import logging
from logging import Logger
import requests

from ui.credentials import credentials_prompt
from ui.warning import warning_retry_prompt

BASE_URL = 'https://developer.atlassian.com'

def get_auth():
    user_name, password = credentials_prompt()
    
    return base64.b64encode(f'{user_name}:{password}'.encode('utf-8'))

class JiraService:
    auth: str
    log: Logger
    
    def __init__(self):
        log = logging.getLogger('TimeTracking')
        log.setLevel(logging.INFO)
        self.log = log
        
    @property
    def headers(self):
        if not self.auth:
            self.auth = get_auth()
        return { 
                'Authorization' : f'Basic {self.auth}',
                'Content-Type' : 'application/json',
            }
    
    def log_hours(self, issue_num: str, hours: float = 1):
        url = f'{BASE_URL}/rest/api/2/issue/{issue_num}/worklog'
        
        if self.issue_exists(issue_num):
            response = requests.post(url, headers=self.headers, data={'timeSpent': f'{hours}h'})
            if response.status_code == 403:
                self.auth = False
                retry = warning_retry_prompt(f'The credentials provided do not have access to issue {issue_num}, your hours have NOT been logged')
                if retry:
                    self.log_hours(issue_num, hours)                
            elif response.status_code != 201:
                self.log.warn(f'Jira replied with a status of {response.status_code}!')
            
        
    def issue_exists(self, issue_num: str) -> bool:
        url = f'{BASE_URL}/rest/api/2/issue/{issue_num}'
        
        response = requests.get(url, headers=self.headers)
        return response.status_code != 404
