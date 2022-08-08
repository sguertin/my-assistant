import PySimpleGUI as sg
from my_assistant.views.view import View


class CredentialsView(View):
    view: sg.Window

    def __init__(self):
        self.view = sg.Window(
            f"Time Tracking",
            [
                [sg.T(f"Please provide your username and password")],
                [sg.T(f"Username:"), sg.In(key="-USER-")],
                [sg.T(f"Password:"), sg.In(key="-PASSWORD-", password_char="•")],
                [sg.Submit(), sg.Cancel()],
            ],
        )
