import PySimpleGUI as sg

from my_assistant.models.events import Events
from my_assistant.views.view import View


class OkCancelPrompt(View):
    view: sg.Window

    def __init__(self, msg: str):
        self.view = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.T(msg)], [sg.Button(Events.OK, bind_return_key=True), sg.Cancel()]],
        )


class WarningPrompt(View):
    view: sg.Window

    def __init__(self, msg: str):
        self.view = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.T(msg)], [sg.Button(Events.CLOSE, bind_return_key=True)]],
        )


class RetryPrompt(View):
    view: sg.Window

    def __init__(self, msg):
        self.view = sg.Window(
            f"Time Tracking - WARNING",
            [
                [sg.T(msg)],
                [sg.T("Do you want to retry?")],
                [sg.Button(Events.RETRY, bind_return_key=True), sg.Cancel()],
            ],
        )
