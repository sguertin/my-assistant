import PySimpleGUI as sg

def warning_prompt(msg: str):
    sg.Window(f'Time Tracking - WARNING', [
            [sg.T(msg)],
            [sg.Button('Close', bind_return_key=True)]
        ]
    ).read(close=True)

def warning_retry_prompt(msg: str) -> bool:
    event, _ = sg.Window(f'Time Tracking - WARNING', [
            [sg.T(msg)],
            [sg.T('Do you want to retry?')],
            [sg.Button('Retry', bind_return_key=True), sg.Cancel()]
        ]
    ).read(close=True)
    
    return event == 'Retry'        