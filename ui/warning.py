import PySimpleGUIQt as sg

def warning_prompt(msg: str):
    sg.Window(f'Time Tracking - WARNING',
        [
            [sg.T(msg)],
            [sg.Submit('Close')]
        ]
    ).read(close=True)

def warning_retry_prompt(msg: str) -> bool:
    event, _ = sg.Window(f'Time Tracking - WARNING',
        [
            [sg.T(msg)],
            [sg.T('Do you want to retry?')],
            [sg.Submit('Retry'), sg.Cancel()]
        ]
    ).read(close=True)
    
    return event == 'Retry'        