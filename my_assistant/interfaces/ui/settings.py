from abc import abstractmethod, ABCMeta

from my_assistant.models.settings import Settings


class IUISettingsService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "set_theme") and callable(subclass.set_theme))
            and (
                hasattr(subclass, "change_settings")
                and callable(subclass.change_settings)
            )
            or NotImplemented
        )

    @abstractmethod
    def change_settings(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change application settings

        Args:
            settings (Settings): The current settings

        Returns:
            Settings: The updated settings
        """
        raise NotImplementedError()

    @abstractmethod
    def set_theme(self, new_theme: str) -> None:
        """Sets the theme color for the UI

        Args:
            new_theme (str): the name of the theme being set
        """
        raise NotImplementedError()
