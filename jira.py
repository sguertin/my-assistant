from dataclasses import dataclass
from datetime import timedelta
import logging
from logging import Logger
import json
from typing import Optional

import requests

from config import get_settings

NEEDS_AUTH_CODE = 901
FAILED_AUTH = 403

@dataclass
class JiraResponse:
    status_code: int
    message: Optional[str] = None

class JiraService:
    auth: str
    base_url: str
    
    def __init__(self, auth: str):
        self.auth = auth
        self.last_status = 0
        self.base_url = get_settings().base_url
        
    @property
    def headers(self) -> dict[str,str]:
        return { 
                'Authorization' : f'Basic {self.auth}',
                'Content-Type' : 'application/json',
                'Accept': 'application/json',
            }
    
    def log_hours(self, issue_num: str, comment: str = None, time_interval: timedelta = None) -> JiraResponse:
        if not time_interval:
            time_interval = timedelta(hours=1)
        if not self.auth:            
            return JiraResponse(NEEDS_AUTH_CODE, 'Need to reauthentication with Jira')
        
        url = f'{self.base_url}/rest/api/2/issue/{issue_num}/worklog'
        
        exists, status_code = self.issue_exists(issue_num)
        if exists:
            data = {'timeSpentSeconds': { time_interval.seconds } }
            if comment:
                data['comment'] = comment
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            
            if response.status_code == 403:
                self.auth = False
                return JiraResponse(response.status_code, 'Authentication with Jira failed!')
            elif response.status_code != 201:
                return JiraResponse(response.status_code, f'Expected status code of 201, got {response.status_code}')
            return JiraResponse(response.status_code)
        else:           
            warning_msg = f'Jira encountered an error attempting to access {issue_num} with a Status Code of {status_code}'
            return JiraResponse(status_code, warning_msg)
    
    def get_url(self, issue_num):
        return f'{self.base_url}/rest/api/2/issue/{issue_num}/worklog'
    
    def issue_exists(self, issue_num: str) -> tuple[bool,int]:
        url = f'{self.base_url}/rest/api/2/issue/{issue_num}'
        
        response = requests.get(url, headers=self.headers)
        
        return response.status_code == 200, response.status_code

class MockJiraService(JiraService):
    log: Logger

    def __init__(self, auth: str):
        self.log = logging.getLogger('MockJiraService')

    def log_hours(self, issue_num: str, comment: str = None, time_interval: timedelta = None) -> JiraResponse:
        if time_interval is None:
            time_interval = timedelta(hours=1)
        request_info = {
            'headers': self.headers,
            'endpoint': self.get_url(issue_num),
            'comment': comment,
            'timeSpentSeconds': time_interval.seconds
        }
        self.log.info(json.dumps(request_info))
        return JiraResponse(201, None)

    def issue_exists(self, issue_num: str) -> tuple[bool,int]:
        return True, 200
