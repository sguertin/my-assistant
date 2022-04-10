from abc import abstractmethod, ABCMeta
from typing import Callable

from my_assistant.models.settings import Settings


class IUIThemeService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "manage_theme") and callable(subclass.manage_theme)
        ) or NotImplemented

    @abstractmethod
    def manage_theme(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change the theme for the application

        Args:
            settings (Settings): The current application settings

        Returns:
            Settings: the updated settings
        """
        raise NotImplementedError()
