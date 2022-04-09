from copy import deepcopy
import time
from logging import Logger
from os import makedirs
import os.path

from my_assistant.constants import HOUR_RANGE, MINUTE_RANGE, SETTINGS_FILE, WORKING_DIR
from my_assistant.exceptions.validation import ValidationError
from my_assistant.interfaces.factories.logfactory import ILoggingFactory
from my_assistant.interfaces.settings import ISettingsService
from my_assistant.models.settings import Settings


class SettingsService(ISettingsService):
    _log: Logger
    _settings: Settings = None
    _last_modified: str = None

    def __init__(self, logging_factory: ILoggingFactory):
        self._log = logging_factory.get_logger("SettingsService")
        if not WORKING_DIR.exists():
            makedirs(WORKING_DIR)

    def get_settings(self) -> Settings:
        if self._settings is None:
            return self.load()
        return deepcopy(self._settings)

    def load(self) -> Settings:
        if not SETTINGS_FILE.exists():
            return self.restore_defaults()
        if self._last_modified is not None:
            last_modified = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(SETTINGS_FILE))
            )
            if last_modified != self._last_modified:
                with open(SETTINGS_FILE, "r") as f:
                    self._settings = Settings.from_json(f.read())
                    self._last_modified = last_modified
        return deepcopy(self._settings)

    def restore_defaults(self) -> Settings:
        self._settings = Settings()
        self.save(self._settings)
        return deepcopy(self._settings)

    def save(self, settings: Settings) -> None:
        try:
            self.validate(settings)
            with open(SETTINGS_FILE, "w+") as f:
                f.write(settings.to_json())
        except IOError as err:
            self._log.error(err)
            raise
        except ValidationError as vex:
            self._log.error(vex)
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
