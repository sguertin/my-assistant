from logging import Logger
import PySimpleGUI as sg

from my_assistant.interfaces.factories.log_factory import ILoggingFactory
from my_assistant.interfaces.ui.warning import IUIWarningService


class UIWarningService(IUIWarningService):
    log: Logger

    def __init__(self, log_factory: ILoggingFactory):
        self.log = log_factory.get_logger("UIWarningService")

    def warning_ok_cancel_prompt(self, msg: str) -> bool:
        event, _ = sg.Window(
            f"Time Tracking - WARNING",
            [[sg.T(msg)], [sg.Button("Proceed", bind_return_key=True), sg.Cancel()]],
        ).read(close=True)
        self.log.info("Event %s received", event)
        return event == "Proceed"

    def warning_prompt(self, msg: str):
        sg.Window(
            f"Time Tracking - WARNING",
            [[sg.T(msg)], [sg.Button("Close", bind_return_key=True)]],
        ).read(close=True)

    def warning_retry_prompt(self, msg: str) -> bool:
        event, _ = sg.Window(
            f"Time Tracking - WARNING",
            [
                [sg.T(msg)],
                [sg.T("Do you want to retry?")],
                [sg.Button("Retry", bind_return_key=True), sg.Cancel()],
            ],
        ).read(close=True)
        self.log.info("Event %s received", event)
        return event == "Retry"
