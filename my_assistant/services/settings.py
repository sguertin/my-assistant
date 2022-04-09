from copy import deepcopy
import time
from logging import Logger
from os import makedirs
import os.path

from my_assistant.constants import HOUR_RANGE, MINUTE_RANGE, SETTINGS_FILE, WORKING_DIR
from my_assistant.exceptions.validation import ValidationError
from my_assistant.interfaces.log_factory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.models.settings import Settings


class SettingsService(ISettingsService):
    log: Logger
    settings: Settings = None
    last_modified: str = None

    def __init__(self, logging_factory: ILoggingFactory):
        self.log = logging_factory.get_logger("SettingsService")
        try:
            if not WORKING_DIR.exists():
                makedirs(WORKING_DIR)
                self.log.info("Created working directory at: %s", WORKING_DIR)
        except OSError as err:
            self.log.error(err)

    def get_settings(self) -> Settings:
        if self.settings is None:
            return self.load()
        return deepcopy(self.settings)

    def load(self) -> Settings:
        try:
            if not SETTINGS_FILE.exists():
                self.log.info(
                    "No settings file found, creating new settings file at %s",
                    SETTINGS_FILE,
                )
                self.last_modified = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(SETTINGS_FILE))
                )
                return self.restore_defaults()
            if self.settings is None:
                self.log.info("Loading settings for first time from %s", SETTINGS_FILE)
                with open(SETTINGS_FILE, "r") as f:
                    self.settings = Settings.from_json(f.read())
                    self.last_modified = time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.localtime(os.path.getmtime(SETTINGS_FILE)),
                    )
            if self.last_modified is not None:
                last_modified = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(SETTINGS_FILE))
                )
                if last_modified != self.last_modified:
                    self.log.info(
                        "File system has more recent version of settings, loading from %s",
                        SETTINGS_FILE,
                    )
                    with open(SETTINGS_FILE, "r") as f:
                        self.settings = Settings.from_json(f.read())
                        self.last_modified = last_modified
            return deepcopy(self.settings)
        except OSError as err:
            self.log.error(err)
            raise

    def restore_defaults(self) -> Settings:
        self.settings = Settings()
        self.save(self.settings)
        return deepcopy(self.settings)

    def save(self, settings: Settings) -> None:
        try:
            self.validate(settings)
            with open(SETTINGS_FILE, "w+") as f:
                f.write(settings.to_json(indent=4))
            self.settings = settings
        except OSError as err:
            self.log.error(err)
            raise
        except ValidationError as vex:
            self.log.error(vex)
            raise

    def validate(self, settings: Settings) -> None:
        error_list: list[str] = []
        if settings.start_hour not in HOUR_RANGE:
            error_list.append(
                f"Start Hour {settings.start_hour:02d} is not between 00 and 23"
            )
        if settings.end_hour not in HOUR_RANGE:
            error_list.append(
                f"End Hour {settings.end_hour:02d} is not between 00 and 23"
            )
        if settings.start_minute not in MINUTE_RANGE:
            error_list.append(
                f"Start Minute {settings.start_minute:02d} is not between 00 and 59"
            )
        if settings.end_minute not in MINUTE_RANGE:
            error_list.append(
                f"End Minute {settings.end_minute:02d} is not between 00 and 59"
            )
        if settings.interval_hours == 0 and settings.interval_minutes == 0:
            error_list.append(f"No time interval specified")
        if settings.work_day < settings.time_interval:
            error_list.append(
                f"Entire workday [{settings.start_hour:02d}:{settings.start_minute:02d}] - "
                + f"[{settings.end_hour:02d}:{settings.end_minute:02d}] = {settings.work_day.hours}h {settings.work_day.minutes}m "
                + f"is less than time recording interval: {settings.interval_hours}h {settings.interval_minutes}m"
            )
        if len(error_list) > 0:
            raise ValidationError(error_list)
