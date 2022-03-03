from dataclasses import dataclass

from typing import Optional

@dataclass
class JiraResponse:
    status_code: int
    message: Optional[str] = None