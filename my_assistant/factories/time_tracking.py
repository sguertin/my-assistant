from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.factories.time_tracking import ITimeTrackingFactory
from my_assistant.interfaces.logfactory import ILoggingFactory
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.models.settings import Settings
from my_assistant.services.time_tracking import JiraService, MockTimeTrackingService


class TimeTrackingFactory(ITimeTrackingFactory):
    def get_time_tracking_service(
        self,
        auth_provider: IAuthenticationProvider,
        ui_provider: IUIFacadeService,
        logging_factory: ILoggingFactory,
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
            return JiraService(auth_provider, ui_provider, logging_factory, settings)
        else:
            return MockTimeTrackingService(
                auth_provider, ui_provider, logging_factory, settings
            )
