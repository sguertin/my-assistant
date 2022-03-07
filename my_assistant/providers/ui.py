from datetime import datetime

from my_assistant.interfaces.ui.credentials import IUICredentialsService
from my_assistant.interfaces.ui.issues import IUIIssueService
from my_assistant.interfaces.ui.settings import IUISettingsService
from my_assistant.interfaces.ui.theme import IUIThemeService
from my_assistant.interfaces.ui.time_tracking import IUITimeTrackingService
from my_assistant.interfaces.ui.warning import IUIWarningService

from my_assistant.models.issues import Issue
from my_assistant.models.settings import Settings


class UIFacadeService:
    ui_warning: IUIWarningService
    time_tracking_service: IUITimeTrackingService
    credentials_service: IUICredentialsService
    issue_service: IUIIssueService
    theme_service: IUIThemeService
    settings_service: IUISettingsService

    def __init__(
        self,
        ui_warning: IUIWarningService,
        time_tracking_service: IUITimeTrackingService,
        credentials_service: IUICredentialsService,
        issue_service: IUIIssueService,
        theme_service: IUIThemeService,
        settings_service: IUISettingsService,
    ):
        """Initializes an instance of the UIProvider

        Args:
            ui_warning (IUIWarningService): the UI warning service
            time_tracking_service (IUITimeTrackingService): the UI time tracking service
            credentials_service (IUICredentialsService): the UI credentials service
            issue_service (IUIIssueService): the UI issue service
            theme_service (IUIThemeService): the UI theme service
            settings_service (IUISettingsService): the UI settings service
        """
        self.ui_warning = ui_warning
        self.time_tracking_service = time_tracking_service
        self.credentials_service = credentials_service
        self.issue_service = issue_service
        self.theme_service = theme_service
        self.settings_service = settings_service

    def warning_retry_prompt(self, msg: str) -> bool:
        return self.ui_warning.warning_retry_prompt(msg)

    def warning_prompt(self, msg: str) -> None:
        self.ui_warning.warning_prompt(msg)

    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        return self.time_tracking_service.record_time(timestamp)

    def credentials_prompt(self) -> tuple[str, str]:
        return self.credentials_service.credentials_prompt()

    def get_issue_info(self, issues: list[Issue]) -> list[Issue]:
        return self.issue_service.get_issue_info(issues)

    def manage_issues(self) -> tuple[bool, list[Issue]]:
        return self.issue_service.manage_issues()

    def manage_theme(self, settings: Settings) -> Settings:
        return self.theme_service.manage_theme(settings)

    def change_settings(self, settings: Settings) -> Settings:
        return self.settings_service.change_settings(settings)

    def set_theme(self, new_theme: str) -> None:
        self.settings_service.set_theme(new_theme)
