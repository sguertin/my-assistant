from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Issue(DataClassJsonMixin):
    issue_num: str
    description: str
    disabled: bool = False

    def __str__(self):
        return f"{self.issue_num} - {self.description}"
