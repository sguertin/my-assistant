from datetime import timedelta
import logging
from logging import Logger
import json

import requests

from ..interfaces.authentication import IAuthenticationProvider
from ..interfaces.assistant import IAssistant
from ..interfaces.ui import IUIProvider
from ..models.issues import Issue
from ..models.jira import JiraResponse
from ..models.settings import Settings

NEEDS_AUTH_CODE = 901
FAILED_AUTH = 403


class JiraService:
    auth_provider: IAuthenticationProvider
    ui_provider: IUIProvider
    log: Logger
    settings: Settings

    def __init__(self, auth_provider: IAuthenticationProvider, ui_provider: IUIProvider, settings: Settings):
        self.auth_provider = auth_provider
        self.ui_provider = ui_provider
        self.last_status = 0
        self.settings = settings
        self.log = logging.getLogger('JiraService')

    def base_url(self) -> str:
        return self.settings.base_url

    @property
    def headers(self) -> 'dict[str, str]':
        return {
            'Authorization': f'{self.auth_provider.get_auth()}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @property
    def clean_headers(self) -> 'dict[str, str]':
        return {
            'Authorization': f'Basic *******',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def try_log_work(self, issue: Issue, comment: str = None, time_interval: timedelta = None) -> None:
        if time_interval is None:
            time_interval = self.settings.time_interval
        response = self.log_hours(issue, comment, time_interval)
        if response.status_code != 201:
            self.log.warning(
                f'Received Response Code: {response.status_code} Message: {response.message}')
            retry = self.ui_provider.warning_retry_prompt(
                f'Received unexpected response from Jira: HttpStatusCode: {response.status_code} Message: "{response.message}"')
            if retry:
                if response.status_code in [NEEDS_AUTH_CODE, FAILED_AUTH]:
                    credentials = self.ui_provider.credentials_prompt()
                    self.auth_provider.set_auth(credentials)
                return self.try_log_work(issue, comment)
        self.log.debug(response)

    def log_hours(self, issue_num: str, comment: str = None, time_interval: timedelta = None) -> JiraResponse:
        if not time_interval:
            time_interval = timedelta(
                hours=self.settings.interval_hours, minutes=self.settings.interval_minutes)
        if not self.auth_provider.get_auth():
            self.log.debug('Credentials not found')
            return JiraResponse(NEEDS_AUTH_CODE, 'Need to reauthenticate with Jira')

        url = f'{self.base_url}/rest/api/2/issue/{issue_num}/worklog'

        exists, status_code = self.issue_exists(issue_num)
        if exists:
            data = {'timeSpentSeconds': {time_interval.seconds}}
            if comment:
                data['comment'] = comment
            self.log.debug(
                f'POST({url}, headers={self.clean_headers}, data={json.dumps(data)})')
            response = requests.post(
                url, headers=self.headers, data=json.dumps(data))

            if response.status_code == 403:
                self.auth_provider.clear_auth()
                return JiraResponse(response.status_code, 'Authentication with Jira failed!')
            elif response.status_code != 201:
                return JiraResponse(response.status_code, f'Expected status code of 201, got {response.status_code}')
            return JiraResponse(response.status_code)
        else:
            warning_msg = f'Jira encountered an error attempting to access {issue_num} with a Status Code of {status_code}'
            return JiraResponse(status_code, warning_msg)

    def get_url(self, issue_num):
        return f'{self.base_url}/rest/api/2/issue/{issue_num}/worklog'

    def issue_exists(self, issue_num: str) -> 'tuple[bool, int]':
        url = f'{self.base_url}/rest/api/2/issue/{issue_num}'
        self.log.debug(f'GET({url}, headers={self.clean_headers})')
        response = requests.get(url, headers=self.headers)

        return response.status_code == 200, response.status_code


class MockTimeTrackingService(IAssistant):
    auth: str
    settings: Settings

    def __init__(self, auth: str, settings: Settings):
        self.auth = auth
        self.settings = settings
        pass

    def try_log_work(self, issue: Issue, comment: str, time_interval: timedelta = None) -> None:
        pass


def get_time_tracking_service(auth_provider: IAuthenticationProvider, ui_provider: IUIProvider, settings: Settings):
    if settings.enable_jira:
        return JiraService(auth_provider, ui_provider, settings)
    else:
        return MockTimeTrackingService('', settings)


def debug_log_hours(jira_service: JiraService, issue_num: str, comment: str = None, time_interval: timedelta = None) -> JiraResponse:
    if time_interval is None:
        time_interval = timedelta(hours=1)
    request_info = {
        'headers': jira_service.headers,
        'endpoint': jira_service.get_url(issue_num),
        'comment': comment,
        'timeSpentSeconds': time_interval.seconds
    }
    jira_service.log.debug(json.dumps(request_info))
    return JiraResponse(201, 'This is a fake Jira Response!')
