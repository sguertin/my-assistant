from datetime import timedelta

from my_assistant.interfaces.base import Interface
from my_assistant.models.issues import Issue


class ITimeTrackingService(Interface):

    def try_log_work(self, workitem: Issue, comment: str = None, time_interval: timedelta = None) -> None:
        """Attempts to make a time entry for a standard interval of work

        Args:
            workitem (Issue): The work item identifier to record log against
            comment (str, optional): Optional comment to include in worklog entry. Defaults to None.
            time_interval (timedelta, optional): The amount of time being logged. Defaults to None (will use standard time interval from settings). 
        """
        pass
