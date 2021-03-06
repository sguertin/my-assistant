from abc import ABCMeta, abstractmethod, abstractstaticmethod
from datetime import datetime
from threading import Semaphore
from typing import Optional


class IAssistant(metaclass=ABCMeta):
    """interface IAssistant - Assistant Service for handling decision making on time recording activities"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "is_work_day") and callable(subclass.is_work_day))
            and (hasattr(subclass, "is_work_time") and callable(subclass.is_work_time))
            and (hasattr(subclass, "is_workhour") and callable(subclass.is_work_hour))
            and (hasattr(subclass, "run") and callable(subclass.run))
            and (hasattr(subclass, "main_prompt") and callable(subclass.main_prompt))
            and (hasattr(subclass, "get_next") and callable(subclass.get_next))
            or NotImplemented
        )

    @abstractstaticmethod
    def is_work_day(date: datetime) -> bool:
        """Checks if the date provided is a workday

        Args:
            date (datetime): The date to check for being a workday

        Returns:
            bool: True if the date is a workday
        """
        raise NotImplementedError()

    @abstractmethod
    def is_work_time(self, time_of_day: datetime = None) -> bool:
        """Determines if a given time is a work time

        Args:
            time_of_day (datetime, optional): The time of day that needs to be determined if it's during work hours. Defaults to None.

        Returns:
            bool: True if time_of_day is within work hours
        """
        raise NotImplementedError()

    @abstractmethod
    def is_work_hour(self, date: Optional[datetime] = None) -> bool:
        """Determines if the given time (now by default) is within working hours

        Args:
            time_of_day (datetime, optional): The time of day that needs to be determined if it's during work hours. Defaults to None.

        Returns:
            bool: True if time_of_day is within work hours
        """
        raise NotImplementedError()

    @abstractmethod
    def run(self) -> None:
        """Runs to test if it's time to record a new entry and record the new entry if so"""
        pass

    @abstractmethod
    def main_prompt(self, timestamp: datetime, manual_override: bool = False) -> datetime:
        """Brings up the Time Entry Prompt for the timestamp provided

        Args:
            timestamp (datetime): the timestamp being recorded
            manual_override (bool): indicates if this entry was called for manually

        Returns:
            datetime: the next time it will take a record
        """
        raise NotImplementedError()

    @abstractmethod
    def get_next(self, now: Optional[datetime] = None) -> datetime:
        """Calculates the next time an entry should be recorded

        Args:
            now (datetime, optional): The time of day to calculate from. Defaults to None.

        Returns:
            datetime: The next time an entry will need to be taken
        """
        raise NotImplementedError()
