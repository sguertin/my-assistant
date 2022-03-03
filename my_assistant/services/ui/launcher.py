from datetime import datetime
from typing import Callable

import PySimpleGUI as sg
from my_assistant.interfaces.assistant import IAssistant
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.models.settings import Settings


class LauncherService:
    assistant: IAssistant
    ui_provider: IUIProvider
    settings: Settings

    def __init__(self, assistant: IAssistant, ui_provider: IUIProvider, settings: Settings):
        self.assistant = assistant
        self.settings = settings
        self.ui_provider = ui_provider

    def run_main_window(self, factory: Callable[[], 'tuple[IAssistant, IUIProvider, Settings]']) -> None:
        window = sg.Window(f'Time Tracking Assistant', [
            [
                [sg.Button('Record Time Now', key='Record')],
                [sg.Button('Manage Issues', key='Issues')],
                [sg.Button('Change Theme', key='Theme')],
                [sg.Button('Settings')],
                [sg.Button('Close')],
            ]
        ])
        while True:
            event, _ = window.read(timeout=30000)
            if event == 'Record':
                self.assistant.main_prompt(datetime.now())
            elif event == 'Issues':
                self.ui_provider.manage_issues()
            elif event == 'Settings':
                self.ui_provider.change_settings(self.settings)
            elif event == 'Theme':
                self.ui_provider.manage_theme(self.settings)
            elif event == 'Close':
                window.close()
                break
            if event in ('Settings', 'Theme'):
                assistant, ui_provider, settings = factory()  # Regenerate dependencies
                self.assistant = assistant
                self.ui_provider = ui_provider
                self.settings = settings

            self.assistant.run()
