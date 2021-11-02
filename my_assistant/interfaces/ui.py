from datetime import datetime
from ..models.issues import Issue


class IUIProvider:
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

    def record_time(self, timestamp: datetime) ->' tuple[Issue, str]':
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
