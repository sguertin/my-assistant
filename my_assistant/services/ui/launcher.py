from datetime import datetime
from logging import Logger

import PySimpleGUI as sg

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.factories.dependencies import IDependencyFactory
from my_assistant.interfaces.logfactory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.interfaces.ui.launcher import IUILauncherService
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
        window = sg.Window(
            title=f"Time Tracking Assistant",
            layout=[
                [sg.Button("Record Time Now", key="Record")],
                [sg.Button("Manage Issues", key="Issues")],
                [sg.Button("Change Theme", key="Theme")],
                [sg.Button("Settings")],
                [sg.Button("Close")],
            ],
            size=(300, 300),
        )
        while True:
            event, _ = window.read(timeout=30000)
            self.log.info("Event %s received", event)
            if event == "Record":
                self.assistant.main_prompt(datetime.now())
            elif event == "Issues":
                self.ui_provider.manage_issues()
            elif event == "Settings":
                self.ui_provider.change_settings(self.settings)
            elif event == "Theme":
                self.ui_provider.manage_theme(self.settings)
            elif event == "Close":
                window.close()
                break
            if event in ("Settings", "Theme"):
                (
                    assistant,
                    ui_provider,
                    settings_service,
                ) = self.dependency_factory.create_dependencies()
                self.assistant = assistant
                self.ui_provider = ui_provider
                self.settings = settings_service.get_settings()

            self.assistant.run()
