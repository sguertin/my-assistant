from datetime import datetime
import logging
from typing import Callable, Optional

from my_assistant.events import CLOSE_EVENTS, ISSUES_EVENT, RECORD_EVENT, SETTINGS_EVENT, THEME_EVENT
from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.launcher import ILauncherService
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.models.settings import Settings


class LauncherService(ILauncherService):
    """Creates the UI for the launcher and handles input
    """
    assistant: IAssistant
    ui_provider: IUIProvider
    settings: Settings

    def __init__(self,
                 assistant: IAssistant,
                 ui_provider: IUIProvider,
                 settings: Settings,
                 factory: Callable[[Optional[Settings]], tuple[IAssistant, IUIProvider]]):
        """Initialize the Launcher

        Args:
            assistant (IAssistant): The assistant service
            ui_provider (IUIProvider): The ui provider
            settings (Settings): the application settings
            factory (Callable[[], tuple[IAssistant, IUIProvider]]): factory function to regenerate dependencies
        """
        self.assistant = assistant
        self.settings = settings
        self.ui_provider = ui_provider
        self.factory = factory
        self.log = logging.getLogger('Launcher')
        self.log.setLevel(settings.log_level)

    def run_main_window(self) -> None:
        self.ui_provider.create_launcher_ui(self.event_handler)

    def event_handler(self, event) -> bool:
        self.log.debug(f'Event: {event}')
        if event == RECORD_EVENT:
            self.assistant.main_prompt(datetime.now())
        elif event == ISSUES_EVENT:
            self.ui_provider.manage_issues()
        elif event in (SETTINGS_EVENT, THEME_EVENT):
            if event == SETTINGS_EVENT:
                self.settings = self.ui_provider.change_settings(self.settings)
            elif event == THEME_EVENT:
                self.settings = self.ui_provider.manage_theme(self.settings)
            assistant, ui_provider = self.factory(
                self.settings)  # Regenerate dependencies
            self.assistant = assistant
            self.ui_provider = ui_provider
        elif event in CLOSE_EVENTS:
            return False
        self.assistant.run()
        return True
