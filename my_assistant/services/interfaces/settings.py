from abc import ABCMeta, abstractmethod
from my_assistant.models.settings import Settings


class ISettingsService(metaclass=ABCMeta):
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "load") and callable(subclass.load))
            and (
                hasattr(subclass, "restore_defaults")
                and callable(subclass.restore_defaults)
            )
            and (hasattr(subclass, "save") and callable(subclass.save))
            and (hasattr(subclass, "validate") and callable(subclass.validate))
            and (hasattr(subclass, "get_settings") and callable(subclass.get_settings))
            or NotImplemented
        )

    @abstractmethod
    def get_settings(self) -> Settings:
        """Retrieves current settings, will load from file system if no settings have been loaded

        Returns:
            Settings: The current settings
        """
        raise NotImplemented()

    @abstractmethod
    def load(self) -> Settings:
        """Loads settings from the default file location

        Returns:
            Settings: The settings loaded from the file system
        """
        raise NotImplemented()

    @abstractmethod
    def restore_defaults(self) -> Settings:
        """Restores the settings to their defaults and saves the settings to the file system

        Returns:
            Settings: the default settings
        """
        pass

    @abstractmethod
    def save(self, settings: Settings) -> None:
        """Saves provided settings to default file location"""
        pass

    @abstractmethod
    def validate(self, settings: Settings) -> list[str]:
        """Validates if the settings provided are valid

        Returns:
            list[str]: List of errors found during validation process
        """
        pass
