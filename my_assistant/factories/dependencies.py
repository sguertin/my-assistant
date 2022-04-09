from my_assistant.constants import LogLevel
from my_assistant.factories.logfactory import LoggingFactory
from my_assistant.factories.time_tracking import TimeTrackingFactory
from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.factories.dependencies import IDependencyFactory
from my_assistant.interfaces.factories.time_tracking import ITimeTrackingFactory
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.logfactory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui.credentials import IUICredentialsService
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.interfaces.ui.issues import IUIIssueService
from my_assistant.interfaces.ui.settings import IUISettingsService
from my_assistant.interfaces.ui.theme import IUIThemeService
from my_assistant.interfaces.ui.warning import IUIWarningService
from my_assistant.providers.authentication import BasicAuthenticationProvider
from my_assistant.providers.ui import UIFacadeService
from my_assistant.services.assistant import Assistant
from my_assistant.services.issues import IssueService
from my_assistant.services.settings import SettingsService
from my_assistant.services.taskfile import TaskFileService
from my_assistant.services.ui.credentials import UICredentialsService
from my_assistant.services.ui.issues import UIIssueService
from my_assistant.services.ui.settings import UISettingsService
from my_assistant.services.ui.theme_browser import UIThemeService
from my_assistant.services.ui.time_tracking import UITimeTrackingService
from my_assistant.services.ui.warning import UIWarningService


class DependencyFactory(IDependencyFactory):
    def create_dependencies(
        self,
    ) -> tuple[IAssistant, IUIFacadeService, ISettingsService]:
        logging_factory: ILoggingFactory = LoggingFactory(LogLevel.INFO)
        settings_service: ISettingsService = SettingsService(logging_factory)

        time_tracking_factory: ITimeTrackingFactory = TimeTrackingFactory()
        task_service: ITaskFileService = TaskFileService()

        auth_provider: IAuthenticationProvider = BasicAuthenticationProvider()
        issue_service: IIssueService = IssueService(logging_factory)
        ui_warning_service: IUIWarningService = UIWarningService(logging_factory)
        ui_issue_service: IUIIssueService = UIIssueService(
            issue_service, ui_warning_service, logging_factory
        )
        ui_time_tracking: ITimeTrackingService = UITimeTrackingService(
            issue_service, ui_issue_service, logging_factory
        )
        ui_credential_service: IUICredentialsService = UICredentialsService(
            logging_factory
        )

        ui_theme_service: IUIThemeService = UIThemeService(logging_factory)
        ui_settings_service: IUISettingsService = UISettingsService(
            ui_warning_service, settings_service, logging_factory
        )
        ui_service: IUIFacadeService = UIFacadeService(
            ui_warning_service,
            ui_time_tracking,
            ui_credential_service,
            ui_issue_service,
            ui_theme_service,
            ui_settings_service,
        )
        time_tracking: ITimeTrackingService = (
            time_tracking_factory.get_time_tracking_service(
                auth_provider, ui_service, logging_factory, settings_service
            )
        )

        assistant: IAssistant = Assistant(
            time_tracking,
            ui_service,
            task_service,
            issue_service,
            logging_factory,
            settings_service,
        )
        return assistant, ui_service, settings_service
