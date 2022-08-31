from dataclasses import dataclass, field
from datetime import timedelta, datetime

from dataclasses_json import DataClassJsonMixin

from my_assistant.constants import LogLevel


@dataclass(slots=True)
class Settings(DataClassJsonMixin):
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
        if self.start_hour > self.end_hour >= now.hour:
            return datetime(
                now.year, now.day, now.month, self.start_hour, self.start_minute, 0
            ) - timedelta(days=1)
        return datetime(
            now.year, now.day, now.month, self.start_hour, self.start_minute, 0
        )

    @property
    def end_time(self) -> datetime:
        now = datetime.now()
        if self.start_hour > self.end_hour >= now.hour:
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

    def __str__(self):
        return self.to_json(indent=4)
