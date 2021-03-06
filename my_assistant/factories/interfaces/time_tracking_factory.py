from abc import ABCMeta, abstractmethod
from my_assistant.models.settings import Settings
from my_assistant.providers.interfaces.authentication import IAuthenticationProvider
from my_assistant.factories.interfaces.log_factory import ILoggingFactory

from my_assistant.services.interfaces.time_tracking import ITimeTrackingService
from my_assistant.services.interfaces.ui_facade import IUIFacadeService


class ITimeTrackingFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_time_tracking_service")
            and callable(subclass.get_time_tracking_service)
        ) or NotImplemented

    @abstractmethod
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
        raise NotImplementedError()
