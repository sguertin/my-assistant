from dataclasses import dataclass, field
from datetime import timedelta
import logging

from dataclasses_json import dataclass_json, LetterCase

from my_assistant.constants import SETTINGS_FILE


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Settings:
    theme: str = 'DarkBlue3'
    base_url: str = ''
    start_hour: int = 8
    start_minute: int = 0
    end_hour: int = 17
    end_minute: int = 0
    interval_hours: int = 1
    interval_minutes: int = 0
    enable_jira: bool = True
    log_level: int = logging.INFO
    days_of_week: frozenset[int] = field(
        default_factory=lambda: frozenset(0, 1, 2, 3, 4))

    @property
    def time_interval(self) -> timedelta:
        return timedelta(
            hours=self.interval_hours,
            minutes=self.interval_minutes
        )

    @classmethod
    def restore_defaults(cls) -> 'Settings':
        """Restores the settings to their default

        Returns:
            Settings: the default settings
        """
        settings = cls()
        settings.save()
        return settings

    @classmethod
    def load(cls) -> 'Settings':
        """Loads the settings from the local settings file

        Returns:
            Settings: Returns the settings in the save file
        """
        if not SETTINGS_FILE.exists():
            return cls.restore_defaults()
        with open(SETTINGS_FILE, 'r') as f:
            return cls.from_json(f.read())

    def save(self) -> None:
        """Saves current settings to configuration file

        """
        with open(SETTINGS_FILE, 'w') as f:
            f.write(self.to_json())
