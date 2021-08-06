import PySimpleGUI as sg

from config import get_settings


def run_main_window() -> None:
    window = sg.Window(f'Time Tracking Assistant', [
        [
            sg.Button('Record Time Now', key='Record'),
            sg.Button('Settings'),
            sg.Button('Close'),
        ]
    ])

    while True:
        event, _ = window.read()
        if event == 'Record':
            pass
        elif event == 'Settings':
            pass
        else:
            window.close()
            break
