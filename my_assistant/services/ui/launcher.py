from datetime import datetime

import PySimpleGUI as sg

from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.dependencies import IDependencyFactory
from my_assistant.interfaces.ui.facade import IUIFacadeService
from my_assistant.interfaces.ui.launcher import ILauncherService
from my_assistant.models.settings import Settings


class LauncherService(ILauncherService):
    assistant: IAssistant
    ui_provider: IUIFacadeService
    dependency_factory: IDependencyFactory
    settings: Settings

    def __init__(
        self,
        assistant: IAssistant,
        ui_provider: IUIFacadeService,
        dependency_factory: IDependencyFactory,
        settings: Settings,
    ):
        self.assistant = assistant
        self.settings = settings
        self.dependency_factory = dependency_factory
        self.ui_provider = ui_provider

    def run_main_window(self) -> None:
        window = sg.Window(
            f"Time Tracking Assistant",
            [
                [
                    [sg.Button("Record Time Now", key="Record")],
                    [sg.Button("Manage Issues", key="Issues")],
                    [sg.Button("Change Theme", key="Theme")],
                    [sg.Button("Settings")],
                    [sg.Button("Close")],
                ]
            ],
        )
        while True:
            event, _ = window.read(timeout=30000)
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
                    settings,
                ) = self.dependency_factory.create_dependencies()
                self.assistant = assistant
                self.ui_provider = ui_provider
                self.settings = settings

            self.assistant.run()
