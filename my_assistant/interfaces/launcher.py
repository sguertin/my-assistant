

from typing import Any, Callable

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.models.settings import Settings


class ILauncherService:
    """Creates the UI for the launcher and handles input
    """

    def __init__(self,
                 assistant: IAssistant,
                 ui_provider: IUIProvider,
                 settings: Settings,
                 factory: Callable[[], tuple[IAssistant, IUIProvider, Settings]]):
        raise TypeError("Interfaces cannot be initialized!")

    def run_main_window(self) -> None:
        """Runs main application window
        """
        raise NotImplementedError('This method is not implemented')

    def event_handler(self, event: str) -> bool:
        """Handles events received by the UI

        Args:
            event (str): The triggering event

        Returns:
            bool: True if the application should close, otherwise it returns False
        """
        raise NotImplementedError('This method is not implemented')
