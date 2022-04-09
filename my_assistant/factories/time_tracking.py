from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.factories.time_tracking import ITimeTrackingFactory
from my_assistant.interfaces.factories.log_factory import ILoggingFactory
from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.services.time_tracking import JiraService, MockTimeTrackingService


class TimeTrackingFactory(ITimeTrackingFactory):
    def get_time_tracking_service(
        self,
        auth_provider: IAuthenticationProvider,
        ui_provider: IUIFacadeService,
        logging_factory: ILoggingFactory,
        settings_service: ISettingsService,
    ) -> ITimeTrackingService:
        settings = settings_service.get_settings()
        if settings.enable_jira:
            return JiraService(
                auth_provider, ui_provider, logging_factory, settings_service
            )
        else:
            return MockTimeTrackingService(
                auth_provider, ui_provider, logging_factory, settings_service
            )
