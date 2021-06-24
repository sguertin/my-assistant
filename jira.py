import base64
import json
import logging
from logging import Logger
import requests

from ui.credentials import credentials_prompt
from ui.warning import warning_prompt, warning_retry_prompt

BASE_URL = 'https://jira.housingcenter.com'

def get_auth():
    user_name, password = credentials_prompt()
    encoding = base64.b64encode(f'{user_name}:{password}'.encode('utf-8'))
    
    return str(encoding).replace("b'", "").replace("'", "")

class JiraService:
    auth: str
    log: Logger
    last_status: int
    
    def __init__(self):
        log = logging.getLogger('TimeTracking')
        log.setLevel(logging.INFO)
        self.log = log
        self.auth = get_auth()
        self.last_status = 0
        
    @property
    def headers(self):
        if not self.auth:
            self.auth = get_auth()
        return { 
                'Authorization' : f'Basic {self.auth}',
                'Content-Type' : 'application/json',
                'Accept': 'application/json',
            }
    
    def log_hours(self, issue_num: str, hours: float = 1):
        url = f'{BASE_URL}/rest/api/2/issue/{issue_num}/worklog'
        
        if self.issue_exists(issue_num):
            data = json.dumps({'timeSpent': f'{hours}h'})
            response = requests.post(url, headers=self.headers, data=data)
            self.last_status = response.status_code
            
            if response.status_code == 403:
                self.auth = False
                retry = warning_retry_prompt(f'The credentials provided do not have access to issue {issue_num}, your hours have NOT been logged')
                if retry:
                    self.log_hours(issue_num, hours)

            elif response.status_code != 201:
                warning_msg = f'Jira replied with a status of {self.last_status}!'
                self.log.warn(warning_msg)
                warning_prompt(warning_msg)
        else:
            warning_msg = f'Jira encountered an error attempting to access {issue_num} with a Status Code of {self.last_status}'
            self.log.warn(warning_msg)
            warning_prompt(warning_msg)

    def issue_exists(self, issue_num: str) -> bool:
        url = f'{BASE_URL}/rest/api/2/issue/{issue_num}'
        
        response = requests.get(url, headers=self.headers)
        self.last_status = response.status_code
        
        return response.status_code == 200
