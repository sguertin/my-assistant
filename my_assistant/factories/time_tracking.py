from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.models.settings import Settings
from my_assistant.services.time_tracking import JiraService, MockTimeTrackingService


class TimeTrackingFactory:
    @classmethod
    def get_time_tracking_service(
        cls,
        auth_provider: IAuthenticationProvider,
        ui_provider: IUIFacadeService,
        settings: Settings,
    ) -> ITimeTrackingService:
        """Constructs an instance of the TimeTrackingService

        Args:
            auth_provider (IAuthenticationProvider): The authentication provider
            ui_provider (IUIProvider): the ui provider
            settings (Settings): the application settings

        Returns:
            ITimeTrackingService: the constructed TimeTrackingService
        """
        if settings.enable_jira:
            return JiraService(auth_provider, ui_provider, settings)
        else:
            return MockTimeTrackingService(auth_provider, ui_provider, settings)
