from dataclasses import dataclass

from typing import Optional

from dataclasses_json import DataClassJsonMixin


@dataclass(slots=True)
class JiraResponse(DataClassJsonMixin):
    status_code: int
    message: Optional[str] = None
