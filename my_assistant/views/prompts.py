import PySimpleGUI as sg

from my_assistant.models.events import Events
from my_assistant.views.view import View


class PromptView(View):
    def read(self, close: bool = True) -> str:
        event, _ = self.window.read(close=close)
        return event


class OkCancelPrompt(PromptView):
    window: sg.Window

    def __init__(self, msg: str):
        self.window = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.Text(msg)], [sg.Button(Events.OK, bind_return_key=True), sg.Cancel()]],
        )


class WarningPrompt(PromptView):
    window: sg.Window

    def __init__(self, msg: str):
        self.window = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.Text(msg)], [sg.Button(Events.CLOSE, bind_return_key=True)]],
        )


class RetryPrompt(PromptView):
    window: sg.Window

    def __init__(self, msg):
        self.window = sg.Window(
            f"Time Tracking - WARNING",
            [
                [sg.Text(msg)],
                [sg.Text("Do you want to retry?")],
                [sg.Button(Events.RETRY, bind_return_key=True), sg.Cancel()],
            ],
        )
