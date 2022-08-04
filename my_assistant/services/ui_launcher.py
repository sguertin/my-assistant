from datetime import datetime
from logging import Logger

import PySimpleGUI as sg

from my_assistant.services.interfaces.assistant import IAssistant
from my_assistant.factories.interfaces.dependency_factory import IDependencyFactory
from my_assistant.factories.interfaces.log_factory import ILoggingFactory
from my_assistant.services.interfaces.settings import ISettingsService
from my_assistant.services.interfaces.ui_facade import IUIFacadeService
from my_assistant.services.interfaces.ui_launcher import IUILauncherService
from my_assistant.models.settings import Settings

BUTTON_SIZE: tuple[int,int] = (35, 1)
class UILauncherService(IUILauncherService):
    assistant: IAssistant
    ui_provider: IUIFacadeService
    dependency_factory: IDependencyFactory
    settings: Settings
    log: Logger

    def __init__(
        self,
        assistant: IAssistant,
        ui_provider: IUIFacadeService,
        dependency_factory: IDependencyFactory,
        settings_service: ISettingsService,
        log_factory: ILoggingFactory,
    ):
        self.assistant = assistant
        self.settings = settings_service.get_settings()
        self.dependency_factory = dependency_factory
        self.ui_provider = ui_provider
        self.log = log_factory.get_logger("UILauncherService")

    def run_main_window(self) -> None:
        window = sg.Window(
            title=f"Time Tracking Assistant",
            layout=[
                [sg.Button("Record Time Now", key="Record", size=BUTTON_SIZE)],
                [sg.Button("Manage Issues", key="Issues", size=BUTTON_SIZE)],
                [sg.Button("Change Theme", key="Theme", size=BUTTON_SIZE)],
                [sg.Button("Settings", size=BUTTON_SIZE)],
                [sg.Button("Close", size=BUTTON_SIZE)],
            ],
        )        
        try:
            self.assistant.run()
            while True:
                event, _ = window.read(timeout=30000)
                self.log.info("Event %s received", event)
                if event == "Record":
                    self.assistant.main_prompt(datetime.now(), True)                   
                elif event == "Issues":
                    self.ui_provider.manage_issues()
                elif event == "Settings":
                    self.ui_provider.change_settings(self.settings)
                elif event == "Theme":
                    self.ui_provider.manage_theme(self.settings)
                elif event in (sg.WIN_CLOSED, "Close"):
                    window.close()
                    break
                else:
                    self.assistant.run()
        except Exception as ex:
            self.log.exception(ex)
            raise

    def _run_assistant(self):
        self.log.debug("Thread calling for assistant to")
        self.assistant.run()

    def update_dependencies(self, settings: Settings):
        (
            assistant,
            ui_provider,
            settings_service,
            log_factory,
        ) = self.dependency_factory.create_dependencies(settings)
        self.assistant = assistant
        self.ui_provider = ui_provider
        self.settings = settings_service.get_settings()
        self.log = log_factory.get_logger("UILauncher")
