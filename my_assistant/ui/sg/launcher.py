from typing import Callable

import PySimpleGUI as sg

from my_assistant.events import CLOSE_EVENT, ISSUES_EVENT, RECORD_EVENT, SETTINGS_EVENT, THEME_EVENT


def create_launcher_ui(self, theme, handler: Callable[[str, str], bool]) -> None:
    sg.theme(theme)
    close = False
    window = sg.Window(f'Time Tracking Assistant', [
        [
            [sg.Button('Record Time Now', key=RECORD_EVENT)],
            [sg.Button('Manage Issues', key=ISSUES_EVENT)],
            [sg.Button('Change Theme', key=THEME_EVENT)],
            [sg.Button('Settings', key=SETTINGS_EVENT)],
            [sg.Button('Close', key=CLOSE_EVENT)],
        ]
    ], size=(300, 200))
    while True:
        event, _ = window.read(timeout=5000)
        close = handler(event)
        if close:
            window.close()
            break
