from typing import Callable

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.launcher import ILauncherService
from my_assistant.interfaces.taskfile import ITaskFileService
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui import IUIProvider

from my_assistant.models.settings import Settings

from my_assistant.providers.authentication import BasicAuthenticationProvider
from my_assistant.providers.ui import UIProvider
from my_assistant.services.assistant import Assistant
from my_assistant.services.issues import IssueService
from my_assistant.services.launcher import LauncherService
from my_assistant.services.taskfile import TaskFileService
from my_assistant.services.time_tracking import JiraService, MockTimeTrackingService


class Factory:
    def __init__(self, settings: Settings = None):
        if settings is None:
            settings = Settings.load()
        self.settings = settings

    def create_launcher_dependencies(self, settings: Settings = None) -> tuple[IAssistant, IUIProvider]:
        if settings is None:
            settings = self.settings

        auth_provider = self.get_auth_provider()
        ui_provider = self.get_ui_provider()
        issue_service = self.get_issue_service(ui_provider)
        task_service = self.get_task_file_service(settings)
        time_tracking = self.get_time_tracking_service(
            auth_provider, ui_provider, settings)
        assistant = self.get_assistant(
            time_tracking, ui_provider, task_service, issue_service, settings)
        return assistant, ui_provider

    def get_auth_provider() -> IAuthenticationProvider:
        return BasicAuthenticationProvider()

    def get_launcher_service(self,
                             assistant: IAssistant,
                             ui_provider: IUIProvider,
                             settings: Settings = None) -> ILauncherService:
        """Returns initialized instance of ILauncherService

        Args:
            assistant (IAssistant): [description]
            ui_provider (IUIProvider): [description]
            settings (Settings): [description]
            create_dependencies (Callable[[], None]): [description]

        Returns:
            [type]: [description]
        """
        return LauncherService(assistant, ui_provider, settings, self.create_launcher_dependencies)

    def get_assistant(self,
                      time_tracking: ITimeTrackingService,
                      ui_provider: IUIProvider,
                      task_service: ITaskFileService,
                      issue_service: IIssueService,
                      settings: Settings = None) -> IAssistant:
        """Returns initialized instance of IAssistant 

        Args:
            time_tracking (ITimeTrackingService): Service that handles communication with time tracking 
            ui_provider (IUIProvider): Service that provides UI Controls
            task_service (ITaskFileService): Service that handles the task log
            issue_service (IIssueService): Service that handles the list of active and inactive issues
            settings (Settings): The application settings

        Returns:
            IAssistant: The initialized IAssistant
        """
        if settings is None:
            settings = self.settings
        return Assistant(time_tracking, ui_provider, task_service, issue_service, settings)

    def get_issue_service(self, ui_provider: IUIProvider) -> IIssueService:
        """Gets an initialized instance of IIssueService

        Args:
            ui_provider (IUIProvider): the ui provider for the new IIssueService

        Returns:
            IIssueService: the initialized IIssueService
        """
        return IssueService(ui_provider)

    def get_task_file_service(self, settings: Settings = None) -> ITaskFileService:
        """Returns initialized instance of ITaskFileService

        Args:
            settings (Settings): the application settings

        Returns:
            ITaskFileService: the initialized ITaskFileService
        """
        if settings is None:
            settings = self.settings
        return TaskFileService(settings)

    def get_time_tracking_service(self, auth_provider: IAuthenticationProvider, ui_provider: IUIProvider, settings: Settings = None) -> ITimeTrackingService:
        """Returns an initialized instance of ITimeTrackingService

        Args:
            auth_provider (IAuthenticationProvider): [description]
            ui_provider (IUIProvider): [description]
            settings (Settings): [description]

        Returns:
            [type]: [description]
        """
        if settings is None:
            settings = self.settings
        if settings.enable_jira:
            return JiraService(auth_provider, ui_provider, settings)
        else:
            return MockTimeTrackingService('', settings)

    def get_ui_provider() -> IUIProvider:
        """Returns an initialized instance of IUIProvider

        Returns:
            IUIProvider: [description]
        """
        return UIProvider()
