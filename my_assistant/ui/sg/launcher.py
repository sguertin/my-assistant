from typing import Callable

import PySimpleGUI as sg

from my_assistant.events import CLOSE_EVENT, ISSUES_EVENT, RECORD_EVENT, SETTINGS_EVENT, START_UP_EVENT, THEME_EVENT


def create_launcher_ui(self, theme, handler: Callable[[str, str], bool]) -> None:
    sg.theme(theme)
    window = sg.Window(f'Time Tracking Assistant', [
        [
            [sg.Button('Record Time Now', key=RECORD_EVENT)],
            [sg.Button('Manage Issues', key=ISSUES_EVENT)],
            [sg.Button('Change Theme', key=THEME_EVENT)],
            [sg.Button('Settings', key=SETTINGS_EVENT)],
            [sg.Button('Close', key=CLOSE_EVENT)],
        ]
    ], size=(300, 200))
    event = START_UP_EVENT
    while handler(event):
        event, _ = window.read(timeout=5000)
    window.close()
