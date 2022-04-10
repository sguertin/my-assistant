from datetime import datetime
from logging import Logger
from threading import Thread

import PySimpleGUI as sg

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.dependency_factory import IDependencyFactory
from my_assistant.interfaces.log_factory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.ui_facade import IUIFacadeService
from my_assistant.interfaces.ui_launcher import IUILauncherService
from my_assistant.models.settings import Settings


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
        button_size = (35, 1)
        window = sg.Window(
            title=f"Time Tracking Assistant",
            layout=[
                [sg.Button("Record Time Now", key="Record", size=button_size)],
                [sg.Button("Manage Issues", key="Issues", size=button_size)],
                [sg.Button("Change Theme", key="Theme", size=button_size)],
                [sg.Button("Settings", size=button_size)],
                [sg.Button("Close", size=button_size)],
            ],
        )
        assistant_thread = Thread(target=self._run_assistant)

        try:
            assistant_thread.start()
            while True:
                event, _ = window.read(timeout=30000)
                self.log.info("Event %s received", event)
                if event == "Record":
                    self.log.debug("self.assistant.lock.acquire()")
                    self.assistant.lock.acquire()
                    self.assistant.main_prompt(datetime.now())
                    self.log.debug("self.assistant.lock.release()")
                    self.assistant.lock.release()
                elif event == "Issues":
                    self.ui_provider.manage_issues()
                elif event == "Settings":
                    self.ui_provider.change_settings(self.settings)
                elif event == "Theme":
                    self.ui_provider.manage_theme(self.settings)
                elif event in (sg.WIN_CLOSED, "Close"):
                    window.close()
                    break
        except Exception as ex:
            self.log.exception(ex)
            raise
        finally:
            assistant_thread.join()

    def _run_assistant(self):
        self.log.debug("Thread calling for assistant to")
        self.assistant.run()

    def update_dependencies(
        self,
        assistant: IAssistant,
        ui_provider: IUIFacadeService,
        settings_service: ISettingsService,
        log_factory: ILoggingFactory,
    ):
        self.assistant = assistant
        self.ui_provider = ui_provider
        self.settings = settings_service.get_settings()
        self.log = log_factory.get_logger("UILauncher")
