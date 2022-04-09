from abc import abstractmethod, ABCMeta
from datetime import datetime
from typing import Callable

from my_assistant.models.settings import Settings
from my_assistant.models.issues import Issue


class IUIFacadeService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (
                hasattr(subclass, "warning_retry_prompt")
                and callable(subclass.warning_retry_prompt)
            )
            and (
                hasattr(subclass, "warning_prompt")
                and callable(subclass.warning_prompt)
            )
            and (hasattr(subclass, "record_time") and callable(subclass.record_time))
            and (
                hasattr(subclass, "credentials_prompt")
                and callable(subclass.credentials_prompt)
            )
            and (
                hasattr(subclass, "manage_issues") and callable(subclass.manage_issues)
            )
            and (hasattr(subclass, "manage_theme") and callable(subclass.manage_theme))
            and (
                hasattr(subclass, "change_settings")
                and callable(subclass.change_settings)
            )
            and (hasattr(subclass, "set_theme") and callable(subclass.set_theme))
            or NotImplemented
        )

    @abstractmethod
    def warning_retry_prompt(self, msg: str) -> bool:
        """Gives a warning prompt to the user with a request to retry

        Args:
            msg (str): The warning message to include

        Returns:
            bool: True if Retry is selected
        """
        raise NotImplementedError()

    @abstractmethod
    def warning_prompt(self, msg: str) -> None:
        """Gives basic warning prompt with only the option to continue

        Args:
            msg (str): The warning message to be displayed to the user
        """
        raise NotImplementedError()

    @abstractmethod
    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        """Creates a prompt to capture time worked

        Args:
            timestamp (datetime): The timestamp for the time recording

        Returns:
            tuple[Issue, str]: the issue and a comment
        """
        raise NotImplementedError()

    @abstractmethod
    def credentials_prompt(self) -> "tuple[str, str]":
        """Prompts user to provide credentials

        Returns:
            tuple[str,str]: the credentials entered by the user, ( user, raise NotImplementedError )
        """
        raise NotImplementedError()

    @abstractmethod
    def manage_issues(self) -> tuple[bool, list[Issue]]:
        """Generates a UI Prompt to allow the user to add and remove issues from the list available

        Returns:
            tuple[bool, list[Issue]]: a tuple, True if the user selected 'Save', and the updated list of issues
        """
        raise NotImplementedError()

    @abstractmethod
    def manage_theme(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change the theme for the application

        Args:
            settings (Settings): The current application settings

        Returns:
            Settings: the updated settings
        """
        raise NotImplementedError()

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
        """Sets the color theme for the UI

        Args:
            new_theme (str): the new theme set for the UI
        """
        raise NotImplementedError()
