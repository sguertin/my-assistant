from logging import Logger
import PySimpleGUI as sg

from my_assistant.interfaces.factories.log_factory import ILoggingFactory
from my_assistant.interfaces.ui.credentials import IUICredentialsService


class UICredentialsService(IUICredentialsService):
    log: Logger

    def __init__(self, log_factory: ILoggingFactory):
        self.log = log_factory.get_logger("UICredentialsService")

    def credentials_prompt(self) -> tuple[str, str]:
        window = sg.Window(
            f"Time Tracking",
            [
                [sg.T(f"Please provide your username and password")],
                [sg.T(f"Username:"), sg.In(key="-USER-")],
                [sg.T(f"Password:"), sg.In(key="-PASSWORD-", password_char="•")],
                [sg.Submit(), sg.Cancel()],
            ],
        )
        while True:
            event, values = window.read(close=True)
            self.log.info("Event %s received", event)
            if event == "Submit":
                return values["-USER-"], values["-PASSWORD-"]
            elif event in ("Cancel", sg.WIN_CLOSED):
                return "", ""
