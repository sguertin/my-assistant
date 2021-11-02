from datetime import datetime
from typing import Callable, Any

from models.issues import Issue


class UIProvider:
    def __init__(self, warning_prompt: Callable[[Any, str], None], warning_retry_prompt, record_time: Callable[[Any, str], tuple[Issue, str]], credentials_prompt: Callable[[Any], tuple[str, str]]):
        self.warning_prompt = warning_prompt
        self.record_time = record_time
        self.credentials_prompt = credentials_prompt
        self.warning_retry_prompt = warning_retry_prompt

    def warning_retry_prompt(self, msg: str) -> bool:
        pass

    def warning_prompt(self, msg: str) -> None:
        pass

    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        pass

    def credentials_prompt(self) -> tuple[str, str]:
        pass
