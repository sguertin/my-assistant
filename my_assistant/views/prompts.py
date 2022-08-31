import PySimpleGUI as sg

from my_assistant.models.events import Events
from my_assistant.views.view import View


class PromptView(View):
    def read(self, close: bool = True) -> str:
        event, _ = self.view.read(close=close)
        return event


class OkCancelPrompt(PromptView):
    view: sg.Window

    def __init__(self, msg: str):
        self.view = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.Text(msg)], [sg.Button(Events.OK, bind_return_key=True), sg.Cancel()]],
        )


class WarningPrompt(PromptView):
    view: sg.Window

    def __init__(self, msg: str):
        self.view = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.Text(msg)], [sg.Button(Events.CLOSE, bind_return_key=True)]],
        )


class RetryPrompt(PromptView):
    view: sg.Window

    def __init__(self, msg):
        self.view = sg.Window(
            f"Time Tracking - WARNING",
            [
                [sg.Text(msg)],
                [sg.Text("Do you want to retry?")],
                [sg.Button(Events.RETRY, bind_return_key=True), sg.Cancel()],
            ],
        )
