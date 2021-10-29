from datetime import timedelta, datetime
from logging import Logger

from ..models.settings import Settings

from .jira import IJiraService

class IAssistant:
    """interface IAssistant - Assistant Service for handling decision making on time recording activities
    
        Dependences:
            IJiraService: Jira service to handle interactions with Jira
            Settings: Application configuration state
    """
    def is_workday(self, date: datetime) -> bool:
        """Checks if the date provided is a workday

        Args:
            date (datetime): The date to check for being a workday

        Returns:
            bool: True if the date is a workday
        """
        pass

    def is_workhour(self, date: datetime) -> bool:
        """Determines if the date/time provided is within work hours

        Args:
            date (datetime): The date/time to check for being in work hours

        Returns:
            bool: True if the date/time being checked falls within work hours
        """
        pass
    
    def __init__(self, jira: IJiraService, settings: Settings):
        """Initializes the Assistant

        Args:
            jira (IJiraService): The Jira Service that will handle logging work entries
            settings (Settings): The application settings
        """
        pass

    def run(self) -> None:
        """Runs to test if it's time to record a new entry and record the new entry if so
        """
        pass

    def main_prompt(self, timestamp: datetime) -> datetime:
        """Brings up the Time Entry Prompt for the timestamp provided

        Args:
            timestamp (datetime): the timestamp being recorded

        Returns:
            datetime: the next time it will take a record
        """
        pass

    def get_next(self, now: datetime = None) -> datetime:
        """Calculates the next time an entry should be recorded

        Args:
            now (datetime, optional): The time of day to calculate from. Defaults to None.

        Returns:
            datetime: The next time an entry will need to be taken
        """
        pass