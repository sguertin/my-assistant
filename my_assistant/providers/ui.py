from datetime import datetime
from turtle import update
from typing import Callable

from my_assistant.interfaces.ui.credentials import IUICredentialsService
from my_assistant.interfaces.ui.issues import IUIIssueService
from my_assistant.interfaces.ui.settings import IUISettingsService
from my_assistant.interfaces.ui.theme import IUIThemeService
from my_assistant.interfaces.ui.time_tracking import IUITimeTrackingService
from my_assistant.interfaces.ui.warning import IUIWarningService

from my_assistant.models.issues import Issue
from my_assistant.models.settings import Settings


class UIFacadeService:
    ui_warning_service: IUIWarningService
    ui_time_tracking_service: IUITimeTrackingService
    ui_credentials_service: IUICredentialsService
    ui_issue_service: IUIIssueService
    ui_theme_service: IUIThemeService
    ui_settings_service: IUISettingsService

    def __init__(
        self,
        ui_warning_service: IUIWarningService,
        ui_time_tracking_service: IUITimeTrackingService,
        ui_credentials_service: IUICredentialsService,
        ui_issue_service: IUIIssueService,
        ui_theme_service: IUIThemeService,
        ui_settings_service: IUISettingsService,
    ):
        """Initializes an instance of the UIProvider

        Args:
            ui_warning (IUIWarningService): the UI warning service
            ui_time_tracking_service (IUITimeTrackingService): the UI time tracking service
            ui_credentials_service (IUICredentialsService): the UI credentials service
            ui_issue_service (IUIIssueService): the UI issue service
            ui_theme_service (IUIThemeService): the UI theme service
            ui_settings_service (IUISettingsService): the UI settings service
        """
        self.ui_warning_service = ui_warning_service
        self.ui_time_tracking_service = ui_time_tracking_service
        self.ui_credentials_service = ui_credentials_service
        self.ui_issue_service = ui_issue_service
        self.ui_theme_service = ui_theme_service
        self.ui_settings_service = ui_settings_service

    def warning_retry_prompt(self, msg: str) -> bool:
        return self.ui_warning_service.warning_retry_prompt(msg)

    def warning_prompt(self, msg: str) -> None:
        self.ui_warning_service.warning_prompt(msg)

    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        return self.ui_time_tracking_service.record_time(timestamp)

    def credentials_prompt(self) -> tuple[str, str]:
        return self.ui_credentials_service.credentials_prompt()

    def get_issue_info(self, issues: list[Issue]) -> list[Issue]:
        return self.ui_issue_service.get_issue_info(issues)

    def manage_issues(self) -> tuple[bool, list[Issue]]:
        return self.ui_issue_service.manage_issues()

    def manage_theme(self, settings: Settings) -> Settings:
        return self.ui_theme_service.manage_theme(settings)

    def change_settings(self, settings: Settings) -> Settings:
        return self.ui_settings_service.change_settings(settings)

    def set_theme(self, new_theme: str) -> None:
        self.ui_settings_service.set_theme(new_theme)
