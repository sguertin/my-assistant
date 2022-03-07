from abc import ABCMeta, abstractmethod
from models.settings import Settings
from my_assistant.interfaces.authentication import IAuthenticationProvider
from my_assistant.interfaces.logging import ILoggingFactory

from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui.facade import IUIFacadeService


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
        raise NotImplementedError
