from datetime import datetime
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.taskfile import ITaskFileService

from my_assistant.interfaces.time_tracking import ITimeTrackingService
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.models.settings import Settings


class IAssistant:
    """interface IAssistant - Assistant Service for handling decision making on time recording activities

        Dependencies:
            ITimeTrackingService: Service to handle interactions with Time Tracking Service
            IUIProvider: Provider for creating UI Controls
            ITaskFileService: Service to handle logging task work
            IIssueService: Service for managing issues
            Settings: Application configuration state
    """

    def __init__(self, time_tracking: ITimeTrackingService, ui_provider: IUIProvider, task_service: ITaskFileService, issue_service: IIssueService, settings: Settings):
        raise TypeError("Interface cannot be initialized")

    def run(self) -> None:
        """Runs to test if it's time to record a new entry and record the new entry if so
        """
        raise NotImplementedError('run is not implemented')

    def main_prompt(self, timestamp: datetime) -> datetime:
        """Brings up the Time Entry Prompt for the timestamp provided

        Args:
            timestamp (datetime): the timestamp being recorded

        Returns:
            datetime: the next time it will take a record
        """
        raise NotImplementedError('main_prompt is not implemented')
