
from models.settings import Settings
from my_assistant.factories.logging import LoggingFactory
from my_assistant.factories.time_tracking import TimeTrackingFactory
from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.providers.authentication import BasicAuthenticationProvider
from my_assistant.providers.ui import UIProvider
from my_assistant.services.assistant import Assistant
from my_assistant.services.issues import IssueService
from my_assistant.services.taskfile import TaskFileService
from my_assistant.services.ui.credentials import UICredentialsService
from my_assistant.services.ui.issues import UIIssueService
from my_assistant.services.ui.settings import UISettingsService
from my_assistant.services.ui.theme_browser import UIThemeService
from my_assistant.services.ui.time_tracking import UITimeTrackingService
from my_assistant.services.ui.warning import UIWarningService


class DependencyFactory:

    @staticmethod
    def create_dependencies(settings: 'Settings|None' = None) -> tuple[IAssistant, IUIProvider, Settings]:
        if settings is None:
            settings: Settings = Settings.load()

        auth_provider = BasicAuthenticationProvider()
        logging_factory = LoggingFactory(settings)
        issue_service = IssueService()
        ui_issue_service = UIIssueService()
        warning_service = UIWarningService()
        ui_provider: IUIProvider = UIProvider(
            warning_service=warning_service,
            time_tracking_service=UITimeTrackingService(
                issue_service, ui_issue_service
            ),
            credential_service=UICredentialsService(),
            issue_service=ui_issue_service,
            theme_service=UIThemeService(),
            settings_service=UISettingsService(warning_service)
        )
        task_service = TaskFileService()
        time_tracking = TimeTrackingFactory.get_time_tracking_service(
            auth_provider, ui_provider, settings
        )
        assistant: IAssistant = Assistant(
            time_tracking, ui_provider, task_service, issue_service, logging_factory, settings)
        return assistant, ui_provider, settings
