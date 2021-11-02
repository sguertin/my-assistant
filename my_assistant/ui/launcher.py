from datetime import datetime
from typing import Callable

import PySimpleGUI as sg

from my_assistant.ui.issues import manage_issues
from my_assistant.models.settings import Settings
from my_assistant.services.assistant import Assistant
from my_assistant.ui.settings import change_settings
from my_assistant.ui.theme_browser import manage_theme


class Launcher:
    assistant: Assistant
    settings: Settings

    def __init__(self, assistant: Assistant, settings: Settings):
        self.assistant = assistant
        self.settings = settings

    def run_main_window(self, factory: Callable[[], 'tuple[Assistant, Settings]']) -> None:
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
                manage_issues()
            elif event == 'Settings':
                change_settings(self.settings)
            elif event == 'Theme':
                manage_theme(self.settings)
            elif event == 'Close':
                window.close()
                break
            if event in ('Settings', 'Theme'):
                assistant, settings = factory()  # Regenerate dependencies
                self.assistant = assistant
                self.settings = settings
            self.assistant.run()
