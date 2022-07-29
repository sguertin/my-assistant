from abc import ABCMeta, abstractmethod
from datetime import timedelta
from typing import Optional

from my_assistant.models.issues import Issue


class ITimeTrackingService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "try_log_work") and callable(subclass.try_log_work)
        ) or NotImplemented

    @abstractmethod
    def try_log_work(
        self,
        issue: Issue,
        comment: Optional[str] = None,
        time_interval: Optional[timedelta] = None,
    ) -> None:
        """Attempts to make a time entry for a standard interval of work

        Args:
            issue (Issue): The work item identifier to record log against
            comment (str, optional): Optional comment to include in worklog entry. Defaults to None.
            time_interval (timedelta, optional): The amount of time being logged. Defaults to None (will use standard time interval from settings).
        """
        raise NotImplementedError()
