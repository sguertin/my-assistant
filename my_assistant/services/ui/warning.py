import PySimpleGUI as sg


class UIWarningService:

    def warning_ok_cancel_prompt(self, msg: str) -> bool:
        event, _ = sg.Window(f'Time Tracking - WARNING', [
            [sg.T(msg)],
            [sg.Button('Proceed', bind_return_key=True), sg.Cancel()]
        ]
        ).read(close=True)
        return event == 'Proceed'

    def warning_prompt(self, msg: str):
        sg.Window(f'Time Tracking - WARNING', [
            [sg.T(msg)],
            [sg.Button('Close', bind_return_key=True)]
        ]
        ).read(close=True)

    def warning_retry_prompt(self, msg: str) -> bool:
        event, _ = sg.Window(f'Time Tracking - WARNING', [
            [sg.T(msg)],
            [sg.T('Do you want to retry?')],
            [sg.Button('Retry', bind_return_key=True), sg.Cancel()]
        ]
        ).read(close=True)

        return event == 'Retry'


def warning_ok_cancel_prompt(self, msg: str):
    event, _ = sg.Window(f'Time Tracking - WARNING', [
        [sg.T(msg)],
        [sg.Button('Proceed', bind_return_key=True), sg.Cancel()]
    ]
    ).read(close=True)
    return event == 'Proceed'


def warning_prompt(self, msg: str):
    sg.Window(f'Time Tracking - WARNING', [
        [sg.T(msg)],
        [sg.Button('Close', bind_return_key=True)]
    ]
    ).read(close=True)


def warning_retry_prompt(self, msg: str) -> bool:
    event, _ = sg.Window(f'Time Tracking - WARNING', [
        [sg.T(msg)],
        [sg.T('Do you want to retry?')],
        [sg.Button('Retry', bind_return_key=True), sg.Cancel()]
    ]
    ).read(close=True)

    return event == 'Retry'
