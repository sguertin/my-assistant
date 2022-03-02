from datetime import datetime
from models.settings import Settings

from my_assistant.interfaces.base import Interface
from my_assistant.interfaces.issues import IIssueService
from my_assistant.models.issues import Issue


class IUIProvider(Interface):
    def warning_retry_prompt(self, msg: str) -> bool:
        """Gives a warning prompt to the user with a request to retry

        Args:
            msg (str): The warning message to include

        Returns:
            bool: True if Retry is selected
        """
        pass

    def warning_prompt(self, msg: str) -> None:
        """Gives basic warning prompt with only the option to continue

        Args:
            msg (str): The warning message to be displayed to the user
        """
        pass

    def record_time(self, timestamp: datetime) -> ' tuple[Issue, str]':
        """Creates a prompt to capture time worked

        Args:
            timestamp (datetime): The timestamp for the time recording

        Returns:
            tuple[Issue, str]: the issue and a comment
        """
        pass

    def credentials_prompt(self) -> 'tuple[str, str]':
        """Prompts user to provide credentials

        Returns:
            tuple[str,str]: the credentials entered by the user, ( user, pass )
        """
        pass

    def manage_issues(self) -> tuple[bool, list[Issue]]:
        """Generates a UI Prompt to allow the user to add and remove issues from the list available

        Returns:
            tuple[bool, list[Issue]]: a tuple, True if the user selected 'Save', and the updated list of issues
        """
        pass

    def manage_theme(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change the theme for the application

        Args:
            settings (Settings): The current application settings

        Returns:
            Settings: the updated settings
        """
        pass

    def change_settings(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change application settings

        Args:
            settings (Settings): The current settings

        Returns:
            Settings: The updated settings
        """
        pass

    def set_theme(self, new_theme: str) -> None:
        """Sets the color theme for the UI

        Args:
            new_theme (str): the new theme set for the UI
        """


class IUIWarningService(Interface):

    def warning_ok_cancel_prompt(self, msg: str):
        """Generates a user prompt with a message and proceed/cancel buttons

        Args:
            msg (str): The message to be displayed

        Returns:
            bool: True if the user selects 'Proceed'
        """
        pass

    def warning_prompt(self, msg: str):
        """Generates a user prompt with a message and an ok button

        Args:
            msg (str): The message to be displayed
        """
        pass

    def warning_retry_prompt(self, msg: str) -> bool:
        """Generates a user prompt with a message and retry/cancel buttons

        Args:
            msg (str): The message to be displayed

        Returns:
            bool: True if the user selects 'Retry'
        """
        pass


class IUITimeTrackingService(Interface):

    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        pass


class IUICredentialsService:

    def credentials_prompt(self) -> tuple[str, str]:
        """Generates a user prompt asking for a user name and password

        Returns:
            tuple[str, str]: the username and password
        """
        pass


class IUIIssueService(Interface):

    def get_issue_info(self, issues: list[Issue]) -> list[Issue]:
        """Creates UI control to capture issue information and add to list

        Args:
            issues (list[Issue]): The current list of issues

        Returns:

        """
        pass

    def manage_issues(self) -> tuple[bool, list[Issue]]:
        """Generates a UI Prompt to allow the user to add and remove issues from the list available

        Returns:
            tuple[bool, list[Issue]]: a tuple, True if the user selected 'Save', and the updated list of issues
        """
        pass


class IUIThemeService:
    def manage_theme(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change the theme for the application

        Args:
            settings (Settings): The current application settings

        Returns:
            Settings: the updated settings
        """
        pass


class IUISettingsService:
    def change_settings(self, settings: Settings) -> Settings:
        """Generates a UI Prompt to allow the user to change application settings

        Args:
            settings (Settings): The current settings

        Returns:
            Settings: The updated settings
        """
        pass

    def set_theme(self, new_theme: str) -> None:
        """Sets the theme color for the UI

        Args:
            new_theme (str): the name of the theme being set
        """
        pass
