import PySimpleGUI as sg

from my_assistant.views.view import View
from my_assistant.viewmodels.viewmodel import ViewModel
from my_assistant.viewmodels.credentials import CredentialsViewModel, CredentialKeys


class CredentialsView(View):
    window: sg.Window

    def __init__(self):
        self.viewmodel = CredentialsViewModel()
        self.window = sg.Window(
            f"Time Tracking",
            [
                [sg.Text(f"Please provide your username and password")],
                [sg.Text(f"Username:"), sg.Input(key=CredentialKeys.USERNAME)],
                [
                    sg.Text(f"Password:"),
                    sg.Input(key=CredentialKeys.PASSWORD, password_char="•"),
                ],
                [sg.Submit(), sg.Cancel()],
            ],
        )
