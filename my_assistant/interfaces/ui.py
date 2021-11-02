from datetime import datetime
from typing import Callable

from PySimpleGUI import PySimpleGUI as sg

from my_assistant.models.issues import Issue
from my_assistant.models.settings import Settings


class IUIProvider:
    """Interface for UIProviders
    """

    def change_settings(self, settings: Settings) -> Settings:
        """Creates a UI Prompt for updating application settings

        Args:
            settings (Settings): The current application settings

        Returns:
            Settings: The updated settings
        """
        raise NotImplementedError("change_settings is not implemented")

    def credentials_prompt(self) -> tuple[str, str]:
        """Prompts user to provide credentials

        Returns:
            tuple[str,str]: the credentials entered by the user, ( user, pass )
        """
        raise NotImplementedError("credentials_prompt is not implemented")

    def create_launcher_ui(self, theme,  handler: Callable[[str, str], bool]) -> None:
        """Creates Launcher UI

        Args:
            theme ([type]): The theme for the UI
            handler (Callable[[str, str], bool]): Handler for events on the launcher
        """
        raise NotImplementedError("create_launcher_ui is not implemented")

    def get_issue_info(self, event_handler: Callable[[str, dict], bool]) -> None:
        """Creates a UI Prompt for capturing Issue Info

        Args:            
            event_handler (Callable[[str, dict], bool]): handler to process events from the UI for new issue info

        Returns:
            list[Issue]: The updated list of issues
        """
        raise NotImplementedError("get_issue_info is not implemented")

    def manage_issues(self, issues: list[Issue],
                      deleted_issues: list[Issue],
                      event_handler: Callable[[str, dict], tuple[list[Issue], list[Issue]]]) -> list[Issue]:
        """Creates a UI to manage active and deleted issues

        Args:
            issues (list[Issue]): the active issue list
            deleted_issues (list[Issue]): the inactive issue list
            event_handler (Callable[[str, dict], tuple[list[Issue], list[Issue]]]): the handler to save updated issues

        Returns:
            list[Issue]: the new active issue list
        """
        raise NotImplementedError("manage_issues is not implemented")

    def manage_theme(self, settings: Settings) -> Settings:
        """Provides UI to manage the application theme

        Args:
            settings (Settings): Current application settings

        Returns:
            Settings: Application settings with updated theme
        """
        raise NotImplementedError("manage_theme is not implemented")

    def warning_ok_cancel_prompt(self, msg: str) -> bool:
        """Create a warning prompt with Ok and Cancel options

        Args:
            msg (str): The message to prompt the user         

        Returns:
            bool: True of the user selected 'Proceed'
        """
        raise NotImplementedError(
            'warning_ok_cancel_prompt has not been implemented')

    def warning_prompt(self, msg: str) -> None:
        """Gives basic warning prompt with only the option to continue

        Args:
            msg (str): The warning message to be displayed to the user
        """
        raise NotImplementedError("warning_prompt is not implemented")

    def warning_retry_prompt(self, msg: str) -> bool:
        """Gives a warning prompt to the user with a request to retry

        Args:
            msg (str): The warning message to include

        Returns:
            bool: True if Retry is selected
        """
        raise NotImplementedError("warning_retry_prompt is not implemented")

    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        """Creates a prompt to capture time worked

        Args:
            timestamp (datetime): The timestamp for the time recording

        Returns:
            tuple[Issue, str]: the issue and a comment
        """
        raise NotImplementedError("record_time is not implemented")
