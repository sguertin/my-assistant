from dataclasses import dataclass

from typing import Optional

@dataclass(slots=True)
class JiraResponse:
    status_code: int
    message: Optional[str] = None