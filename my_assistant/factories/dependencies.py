from my_assistant.constants import LogLevel
from my_assistant.factories.log_factory import LoggingFactory
from my_assistant.factories.time_tracking import TimeTrackingFactory
from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.dependency_factory import IDependencyFactory
from my_assistant.interfaces.log_factory import ILoggingFactory
from my_assistant.interfaces.time_tracking_factory import ITimeTrackingFactory
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui_credentials import IUICredentialsService
from my_assistant.interfaces.ui_facade import IUIFacadeService
from my_assistant.interfaces.ui_issues import IUIIssueService
from my_assistant.interfaces.ui_launcher import IUILauncherService
from my_assistant.interfaces.ui_settings import IUISettingsService
from my_assistant.interfaces.ui_theme import IUIThemeService
from my_assistant.interfaces.ui_warning import IUIWarningService
from my_assistant.providers.authentication import BasicAuthenticationProvider
from my_assistant.services.assistant import Assistant
from my_assistant.services.issues import IssueService
from my_assistant.services.settings import SettingsService
from my_assistant.services.taskfile import TaskFileService
from my_assistant.services.ui_credentials import UICredentialsService
from my_assistant.services.ui_facade import UIFacadeService
from my_assistant.services.ui_issues import UIIssueService
from my_assistant.services.ui_launcher import UILauncherService
from my_assistant.services.ui_settings import UISettingsService
from my_assistant.services.ui_theme import UIThemeService
from my_assistant.services.ui_time_tracking import UITimeTrackingService
from my_assistant.services.ui_warning import UIWarningService


class DependencyFactory(IDependencyFactory):
    def create_launcher(self) -> IUILauncherService:
        (
            assistant,
            ui_provider,
            settings_service,
            log_factory,
        ) = self.create_dependencies()
        return UILauncherService(
            assistant, ui_provider, self, settings_service, log_factory
        )

    def create_dependencies(
        self,
    ) -> tuple[IAssistant, IUIFacadeService, ISettingsService, ILoggingFactory]:
        log_factory: ILoggingFactory = LoggingFactory(LogLevel.INFO)
        log = log_factory.get_logger("DependencyFactory")
        try:
            settings_service: ISettingsService = SettingsService(log_factory)
            settings = settings_service.get_settings()
            log_factory.update_level(settings.log_level)
            auth_provider: IAuthenticationProvider = BasicAuthenticationProvider()
            time_tracking_factory: ITimeTrackingFactory = TimeTrackingFactory()

            task_service: ITaskFileService = TaskFileService(log_factory)

            issue_service: IIssueService = IssueService(log_factory)
            ui_warning_service: IUIWarningService = UIWarningService(log_factory)
            ui_issue_service: IUIIssueService = UIIssueService(
                issue_service, ui_warning_service, log_factory
            )
            ui_time_tracking: ITimeTrackingService = UITimeTrackingService(
                issue_service, ui_issue_service, log_factory
            )
            ui_credential_service: IUICredentialsService = UICredentialsService(
                log_factory
            )
            ui_theme_service: IUIThemeService = UIThemeService(
                log_factory, settings_service
            )
            ui_settings_service: IUISettingsService = UISettingsService(
                ui_warning_service, settings_service, log_factory
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
                    auth_provider, ui_service, log_factory, settings_service
                )
            )
            assistant: IAssistant = Assistant(
                time_tracking,
                ui_service,
                task_service,
                issue_service,
                log_factory,
                settings_service,
            )
        except Exception as ex:
            log.exception(ex)
            raise
        return assistant, ui_service, settings_service, log_factory
