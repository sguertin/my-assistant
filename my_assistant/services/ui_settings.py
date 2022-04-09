from logging import Logger
from typing import Callable
import PySimpleGUI as sg
from my_assistant.exceptions.validation import ValidationError
from my_assistant.interfaces.log_factory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.interfaces.ui_settings import IUISettingsService
from my_assistant.interfaces.ui_warning import IUIWarningService
from my_assistant.models.settings import Settings

from my_assistant.constants import (
    HOUR_RANGE,
    MINUTE_RANGE,
    DAYS_OF_WEEK,
    LOGGING_LEVELS,
)


class UISettingsService(IUISettingsService):
    ui_warning_service: IUIWarningService
    settings_service: ISettingsService
    log: Logger

    def __init__(
        self,
        ui_warning_service: IUIWarningService,
        settings_service: ISettingsService,
        log_factory: ILoggingFactory,
    ):
        self.ui_warning_service = ui_warning_service
        self.settings_service = settings_service
        self.log = log_factory.get_logger("UISettingsService")

    @staticmethod
    def set_theme(new_theme) -> None:
        sg.theme(new_theme)

    @staticmethod
    def create_new_settings(values, theme) -> Settings:
        return Settings(
            theme,
            values["base_url"],
            int(values["start_hour"]),
            int(values["start_minute"]),
            int(values["end_hour"]),
            int(values["end_minute"]),
            int(values["interval_hours"]),
            int(values["interval_minutes"]),
            values["enable_jira"],
            LOGGING_LEVELS[values["log_level"]],
            [value for day, value in DAYS_OF_WEEK.items() if values[day]],
        )

    def change_settings(
        self, settings: Settings, update_dependencies: Callable
    ) -> Settings:
        original_settings = Settings.from_dict(settings.to_dict())
        day_checkboxes = []
        for day in DAYS_OF_WEEK.keys():
            day_checkboxes.append(
                sg.Checkbox(
                    day, key=day, default=DAYS_OF_WEEK[day] in settings.days_of_week
                )
            )
        window = sg.Window(
            f"Settings",
            [
                [
                    sg.T("Jira Url (e.g. https://jira.yourcompany.com):"),
                    sg.In(settings.base_url, key="base_url"),
                ],
                [
                    sg.T("Start Time of Day:"),
                    sg.Combo(
                        [f"{hour:02d}" for hour in HOUR_RANGE],
                        default_value=settings.start_hour,
                        key="start_hour",
                    ),
                    sg.T(":"),
                    sg.Combo(
                        [f"{minute:02d}" for minute in MINUTE_RANGE],
                        default_value=settings.start_minute,
                        key="start_minute",
                    ),
                ],
                [
                    sg.T("End Time of Day:"),
                    sg.Combo(
                        [f"{hour:02d}" for hour in HOUR_RANGE],
                        default_value=settings.end_hour,
                        key="end_hour",
                    ),
                    sg.T(":"),
                    sg.Combo(
                        [f"{minute:02d}" for minute in MINUTE_RANGE],
                        default_value=settings.end_minute,
                        key="end_minute",
                    ),
                ],
                [
                    sg.T("Time Recording Interval:"),
                    sg.Combo([0, 1, 2, 3, 4, 5, 6, 7, 8], key="interval_hours"),
                    sg.T("h "),
                    sg.Combo(["00", "15", "30", "45"], key="interval_minutes"),
                    sg.T("m"),
                ],
                [sg.Checkbox("Enable Jira", key="enable_jira")],
                day_checkboxes,
                [sg.Submit("Save"), sg.Button("Cancel")],
            ],
        )
        while True:
            event, values = window.read()
            self.log.info("Event %s received", event)
            if event in ["Submit", "Save"]:
                settings = self.create_new_settings(values, settings.theme)
                try:
                    self.settings_service.save(settings)
                    window.close()
                    return settings
                except ValidationError as err:
                    self.log.error(err)
                    self.ui_warning_service.warning_prompt(err.message)
            elif event in ("Cancel", sg.WINDOW_CLOSED):
                window.close()
                return original_settings

            window.refresh()
