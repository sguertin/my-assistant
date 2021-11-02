from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Issue:
    issue_num: str
    description: str
    disabled: bool = False

    def __eq__(self, other):
        if hasattr(other, 'issue_num'):
            return self.issue_num == other.issue_num
        return self.issue_num == other

    def __str__(self):
        return f'{self.issue_num} - {self.description}'
