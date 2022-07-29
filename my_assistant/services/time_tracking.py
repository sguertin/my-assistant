from datetime import timedelta
import json
from logging import Logger
from typing import Optional

import requests

from my_assistant.constants import (
    JIRA_NEEDS_AUTH_CODE,
    JIRA_FAILED_AUTH,
    JIRA_SUCCESS_RESPONSE,
)
from my_assistant.providers.interfaces.authentication import IAuthenticationProvider
from my_assistant.factories.interfaces.log_factory import ILoggingFactory
from my_assistant.services.interfaces.settings import ISettingsService
from my_assistant.services.interfaces.time_tracking import ITimeTrackingService
from my_assistant.services.interfaces.ui_facade import IUIFacadeService
from my_assistant.models.issues import Issue
from my_assistant.models.jira import JiraResponse
from my_assistant.models.settings import Settings


class JiraService(ITimeTrackingService):
    auth_provider: IAuthenticationProvider
    ui_provider: IUIFacadeService
    log: Logger
    settings: Settings

    def __init__(
        self,
        auth_provider: IAuthenticationProvider,
        ui_provider: IUIFacadeService,
        logging_factory: ILoggingFactory,
        settings_service: ISettingsService,
    ):
        self.auth_provider = auth_provider
        self.ui_provider = ui_provider
        self.last_status = 0
        self.settings = settings_service.get_settings()
        self.log = logging_factory.get_logger("JiraService")

    def base_url(self) -> str:
        return self.settings.base_url

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"{self.auth_provider.get_auth()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @property
    def clean_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Basic *******",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def try_log_work(
        self,
        issue: Issue,
        comment: Optional[str] = None,
        time_interval: Optional[timedelta] = None,
    ) -> None:
        if time_interval is None:
            time_interval = self.settings.time_interval
        response = self.log_hours(issue, comment, time_interval)
        if response.status_code != JIRA_SUCCESS_RESPONSE:
            self.log.warning(
                f"Received Response Code: {response.status_code} Message: {response.message}"
            )
            retry = self.ui_provider.warning_retry_prompt(
                f'Received unexpected response from Jira: HttpStatusCode: {response.status_code} Message: "{response.message}"'
            )
            if retry:
                if response.status_code in [JIRA_NEEDS_AUTH_CODE, JIRA_FAILED_AUTH]:
                    credentials = self.ui_provider.credentials_prompt()
                    self.auth_provider.set_auth(credentials)
                return self.try_log_work(issue, comment)
        self.log.debug(response)

    def log_hours(
        self, issue_num: str, comment: str = None, time_interval: timedelta = None
    ) -> JiraResponse:
        if not time_interval:
            time_interval = timedelta(
                hours=self.settings.interval_hours,
                minutes=self.settings.interval_minutes,
            )
        if not self.auth_provider.get_auth():
            self.log.debug("Credentials not found")
            return JiraResponse(
                JIRA_NEEDS_AUTH_CODE, "Need to reauthenticate with Jira"
            )

        url = f"{self.base_url}/rest/api/2/issue/{issue_num}/worklog"

        exists, status_code = self.issue_exists(issue_num)
        if exists:
            data = {"timeSpentSeconds": {time_interval.seconds}}
            if comment:
                data["comment"] = comment
            self.log.debug(
                "POST(%s, headers=%s, data=%s)",
                url,
                str(self.clean_headers),
                json.dumps(data),
            )
            response = requests.post(url, headers=self.headers, data=json.dumps(data))

            if response.status_code == JIRA_FAILED_AUTH:
                self.auth_provider.clear_auth()
                return JiraResponse(
                    response.status_code, "Authentication with Jira failed!"
                )
            elif response.status_code != JIRA_SUCCESS_RESPONSE:
                return JiraResponse(
                    response.status_code,
                    f"Expected status code of 201, got {response.status_code}",
                )
            return JiraResponse(response.status_code)
        else:
            warning_msg = f"Jira encountered an error attempting to access {issue_num} with a Status Code of {status_code}"
            self.log.warning(
                "Jira encountered an error attempting to access %s with a Status Code of %s",
                issue_num,
                status_code,
            )
            return JiraResponse(status_code, warning_msg)

    def get_url(self, issue_num):
        return f"{self.base_url}/rest/api/2/issue/{issue_num}/worklog"

    def issue_exists(self, issue_num: str) -> "tuple[bool, int]":
        url = f"{self.base_url}/rest/api/2/issue/{issue_num}"
        self.log.debug(f"GET({url}, headers={self.clean_headers})")
        response = requests.get(url, headers=self.headers)

        return response.status_code == 200, response.status_code


class MockTimeTrackingService(ITimeTrackingService):
    log: Logger

    def __init__(
        self,
        auth_provider: IAuthenticationProvider,
        ui_provider: IUIFacadeService,
        logging_factory: ILoggingFactory,
        settings_service: ISettingsService,
    ):
        self.log = logging_factory.get_logger("MockTimeTrackingService")

    def try_log_work(
        self, issue: Issue, comment: str, time_interval: timedelta = None
    ) -> None:
        self.log.debug(
            "Issue: %s, Comment: %s, Time Interval: %s", issue, comment, time_interval
        )
