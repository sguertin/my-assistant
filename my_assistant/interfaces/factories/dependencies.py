from abc import ABCMeta, abstractmethod
from typing import Optional
from models.settings import Settings

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.ui.facade import IUIFacadeService


class IDependencyFactory(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create_dependencies")
            and callable(subclass.create_dependencies)
        ) or NotImplemented

    @abstractmethod
    def create_dependencies(
        self,
        settings: Optional[Settings] = None,
    ) -> tuple[IAssistant, IUIFacadeService, ISettingsService]:
        """Creates Dependencies needed to run the LauncherService

        Args:
            settings (Optional[Settings], optional): The application settings, will load from file system if None. Defaults to None.

        Returns:
            tuple[IAssistant, IUIFacadeService, ISettingsService]: Initialized services needed for Launcher Service
        """
        raise NotImplementedError()
