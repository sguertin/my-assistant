from logging import Logger
import PySimpleGUI as sg
from my_assistant.factories.interfaces.log_factory import ILoggingFactory
from my_assistant.services.interfaces.settings import ISettingsService
from my_assistant.services.interfaces.ui_theme import IUIThemeService
from my_assistant.models.settings import Settings


class UIThemeService(IUIThemeService):
    log: Logger
    settings_service: ISettingsService

    def __init__(
        self, log_factory: ILoggingFactory, settings_service: ISettingsService
    ):
        self.log = log_factory.get_logger("UIThemeService")
        self.settings_service = settings_service

    def manage_theme(self, settings: Settings) -> Settings:
        layout = [
            [sg.Text("Theme Browser")],
            [sg.Text("Click a Theme color to see demo window")],
            [
                sg.Listbox(
                    values=sg.theme_list(),
                    size=(20, 12),
                    key="-LIST-",
                    enable_events=True,
                )
            ],
            [sg.Button("Update"), sg.Button("Exit")],
        ]

        window = sg.Window("Theme Browser", layout)

        while True:  # Event Loop
            event, values = window.read()
            self.log.info("Event %s received", event)
            if event in (sg.WIN_CLOSED, "Exit"):
                sg.theme(settings.theme)
                break
            new_theme = values["-LIST-"][0]
            sg.theme(new_theme)
            sg.popup_get_text(f"This is {new_theme}")
            if event == "Update":
                if settings.theme != new_theme:
                    settings.theme = new_theme
                    self.settings_service.save(settings)
                break

        window.close()
        return settings
