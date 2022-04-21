from abc import ABCMeta, abstractmethod
from datetime import datetime

from my_assistant.models.issues import Issue


class IUITimeTrackingService(metaclass=ABCMeta):
    @abstractmethod
    def record_time(self, timestamp: datetime, manual_override: bool = False) -> tuple[Issue, str]:
        """Generates a UI to capture a new time entry

        Args:
            timestamp (datetime): the timestamp of the entry being captured
            manual_override (bool): indicates if this was a manually requested entry

        Returns:
            tuple[Issue, str]: The issue having time recorded against and the comment
        """
        raise NotImplementedError()
