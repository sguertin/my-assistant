from datetime import timedelta
from logging import Logger


from ..models.jira import JiraResponse
from ..models.issues import Issue
from ..models.settings import Settings


class IJiraService:
    def __init__(self):
        raise TypeError('Cannot initialize an interface!')

    def try_log_work(self, issue: Issue, comment: str = None, time_interval: timedelta = None) -> None:
        """Attempts to make a time entry for a standard interval of work

        Args:
            issue (Issue): The Jira issue number
            comment (str, optional): Optional comment to include in worklog entry. Defaults to None.
            time_interval (timedelta, optional): The amount of time being logged. Defaults to None (will use standard time interval from settings). 
        """
        pass
    
    def log_hours(self, issue_num: str, comment: str = None, time_interval: timedelta = None) -> JiraResponse:
        """Log time against a specified Jira issue, can include a comment and
        variable time interval.

        Args:
            issue_num (str): The Jira Issue numberomment to include with log entry. Defaults to None.
            comment (str, optional): Optional comment to include in worklog entry. Defaults to None.
            time_interval (timedelta, optional): The amount of time being logged. Defaults to None (will use standard time interval from settings).

        Returns:
            JiraResponse: The response receieved from Jira
        """
        pass

    def get_url(self, issue_num: str) -> str:
        """Generates URL for a given Jira Issue provided.

        Args:
            issue_num (str): The Jira issue number            

        Returns:
            str: The URL for the Jira issue number
        """
        pass

    def issue_exists(self, issue_num: str) -> tuple[bool, int]:
        """Checks if a given Jira issue number exists.

        Args:
            issue_num (str): The Jira issue number

        Returns:
            tuple[bool, int]: A tuple of whether it exists (True/False), and the Http Status Code received
        """
        pass
