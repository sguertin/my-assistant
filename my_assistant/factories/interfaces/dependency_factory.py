from abc import ABCMeta, abstractmethod
from typing import Optional

from my_assistant.services.interfaces.assistant import IAssistant
from my_assistant.factories.interfaces.log_factory import ILoggingFactory
from my_assistant.services.interfaces.settings import ISettingsService
from my_assistant.services.interfaces.ui_launcher import IUILauncherService
from my_assistant.services.interfaces.ui_facade import IUIFacadeService
from my_assistant.models.settings import Settings


class IDependencyFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create_dependencies")
            and callable(subclass.create_dependencies),
            hasattr(subclass, "create_launcher") and callable(subclass.create_launcher),
        ) or NotImplemented

    @abstractmethod
    def create_launcher(self) -> IUILauncherService:
        """Creates the launcher service with all it's dependencies

        Returns:
            IUILauncherService: The UI launcher service
        """
        raise NotImplementedError()

    @abstractmethod
    def create_dependencies(
        self,
        settings: Optional[Settings] = None,
    ) -> tuple[IAssistant, IUIFacadeService, ISettingsService, ILoggingFactory]:
        """Creates Dependencies needed to run the UILauncherService

        Args:
            settings (Optional[Settings], optional): The application settings, will load from file system if None. Defaults to None.

        Returns:
            tuple[IAssistant, IUIFacadeService, ISettingsService]: Initialized services needed for Launcher Service
        """
        raise NotImplementedError()
