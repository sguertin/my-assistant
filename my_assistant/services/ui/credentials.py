import PySimpleGUI as sg


class UICredentialsService:
    def credentials_prompt(self) -> tuple[str, str]:
        window = sg.Window(f'Time Tracking', [
            [sg.T(f'Please provide your username and password')],
            [sg.T(f'Username:'), sg.In(key='-USER-')],
            [sg.T(f'Password:'), sg.In(key='-PASSWORD-', password_char='•')],
            [sg.Submit(), sg.Cancel()]
        ]
        )
        while True:
            event, values = window.read(close=True)
            if event == 'Submit':
                return values['-USER-'], values['-PASSWORD-']
            elif event in ('Cancel', sg.WIN_CLOSED):
                return '', ''
