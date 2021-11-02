import PySimpleGUI as sg

from my_assistant.events import CANCEL_EVENT, CLOSE_EVENTS, SUBMIT_EVENT

USER_KEY: str = '-USER-'
PASSWORD_KEY: str = '-PASSWORD-'


def credentials_prompt() -> tuple[str, str]:
    window = sg.Window(f'Time Tracking', [
        [sg.T(f'Please provide your username and password')],
        [sg.T(f'Username:'), sg.In(key=USER_KEY)],
        [sg.T(f'Password:'), sg.In(key=PASSWORD_KEY, password_char='•')],
        [sg.Submit(key=SUBMIT_EVENT), sg.Cancel(key=CANCEL_EVENT)]
    ])
    while True:
        event, values = window.read(close=True)
        if event == SUBMIT_EVENT:
            return values[USER_KEY], values[PASSWORD_KEY]
        elif event in CLOSE_EVENTS:
            return '', ''
