from dataclasses import dataclass, field
from datetime import timedelta, datetime
from os import mkdir

from dataclasses_json import dataclass_json, LetterCase

from my_assistant.constants import (
    HOUR_RANGE,
    MINUTE_RANGE,
    SETTINGS_FILE,
    WORKING_DIR,
    LogLevel,
)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Settings:
    theme: str = "DarkBlue3"
    base_url: str = ""
    start_hour: int = 8
    start_minute: int = 0
    end_hour: int = 17
    end_minute: int = 0
    interval_hours: int = 1
    interval_minutes: int = 0
    enable_jira: bool = True
    log_level: LogLevel = LogLevel.INFO
    days_of_week: frozenset[int] = field(
        default_factory=lambda: frozenset({0, 1, 2, 3, 4})
    )

    @property
    def time_interval(self) -> timedelta:
        return timedelta(hours=self.interval_hours, minutes=self.interval_minutes)

    @property
    def start_time(self) -> datetime:
        now = datetime.now()
        if self.start_hour > self.end_hour and now.hour <= self.end_hour:
            return datetime(
                now.year, now.day, now.month, self.start_hour, self.start_minute, 0
            ) - timedelta(days=1)
        return datetime(
            now.year, now.day, now.month, self.start_hour, self.start_minute, 0
        )

    @property
    def end_time(self) -> datetime:
        now = datetime.now()
        if self.start_hour > self.end_hour and now.hour <= self.end_hour:
            return datetime(
                now.year, now.day, now.month, self.end_hour, self.end_minute, 0
            )
        return datetime(
            now.year, now.day, now.month, self.end_hour, self.end_minute, 0
        ) + timedelta(days=1)

    @property
    def work_day(self) -> timedelta:
        """The duration of a workday

        Returns:
            timedelta: time between start_time and end_time
        """
        return self.end_time - self.start_time

    def validate(self) -> list[str]:
        """Validates if the settings provided are valid

        Returns:
            list[str]: List of errors found during validation process
        """
        error_list = []
        if self.start_hour not in HOUR_RANGE:
            error_list.append(
                f"Start Hour {self.start_hour:02d} is not between 00 and 23"
            )
        if self.end_hour not in HOUR_RANGE:
            error_list.append(f"End Hour {self.end_hour:02d} is not between 00 and 23")
        if self.start_minute not in MINUTE_RANGE:
            error_list.append(
                f"Start Minute {self.start_minute:02d} is not between 00 and 59"
            )
        if self.end_minute not in MINUTE_RANGE:
            error_list.append(
                f"End Minute {self.end_minute:02d} is not between 00 and 59"
            )
        if self.interval_hours == 0 and self.interval_minutes == 0:
            error_list.append(f"No time interval specified")
        if self.work_day < self.time_interval:
            error_list.append(
                f"Entire workday [{self.start_hour:02d}:{self.start_minute:02d}] - "
                + f"[{self.end_hour:02d}:{self.end_minute:02d}] = {self.work_day.hours}h {self.work_day.minutes}m "
                + f"is less than time recording interval: {self.interval_hours}h {self.interval_minutes}m"
            )
        return error_list

    @classmethod
    def restore_defaults(cls) -> "Settings":
        """Restores the settings to their default

        Returns:
            Settings: the default settings
        """
        settings = cls()
        settings.save()
        return settings

    @classmethod
    def load(cls) -> "Settings":
        if not SETTINGS_FILE.exists():
            return cls.restore_defaults()
        with open(SETTINGS_FILE, "r") as f:
            return cls.from_json(f.read())

    def save(self) -> None:
        if not WORKING_DIR.exists():
            mkdir(WORKING_DIR)
        """Saves current settings to configuration file"""
        with open(SETTINGS_FILE, "w") as f:
            f.write(self.to_json())
