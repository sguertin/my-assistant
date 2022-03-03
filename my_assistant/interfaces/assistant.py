from datetime import datetime
from typing import Optional
from my_assistant.interfaces.base import Interface


class IAssistant(Interface):
    """interface IAssistant - Assistant Service for handling decision making on time recording activities

        Dependencies:
            ITimeTrackingService: Service to handle interactions with Time Tracking Service
            Settings: Application configuration state
    """

    @staticmethod
    def is_workday(date: datetime) -> bool:
        """Checks if the date provided is a workday

        Args:
            date (datetime): The date to check for being a workday

        Returns:
            bool: True if the date is a workday
        """
        pass

    def is_work_time(self, time_of_day: datetime = None) -> bool:
        """Determines if a given time is a work time

        Args:
            time_of_day (datetime, optional): The time of day that needs to be determined if it's during work hours. Defaults to None.

        Returns:
            bool: True if time_of_day is within work hours
        """
        pass

    def is_workhour(self, date: Optional[datetime] = None) -> bool:
        """Determines if the given time (now by default) is within working hours

        Args:
            time_of_day (datetime, optional): The time of day that needs to be determined if it's during work hours. Defaults to None.

        Returns:
            bool: True if time_of_day is within work hours
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

    def get_next(self, now: Optional[datetime] = None) -> datetime:
        """Calculates the next time an entry should be recorded

        Args:
            now (datetime, optional): The time of day to calculate from. Defaults to None.

        Returns:
            datetime: The next time an entry will need to be taken
        """
        pass
