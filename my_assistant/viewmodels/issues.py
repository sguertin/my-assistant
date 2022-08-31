from enum import Enum

from my_assistant.models.issues import Issue
from my_assistant.viewmodels.viewmodel import ViewModel


class IssueInformationKeys(Enum):
    ISSUE = "-ISSUE-"
    DESCRIPTION = "-DESCRIPTION-"


class IssueInformationViewModel(ViewModel):
    def load(self, values: dict[str, str]):
        return Issue(
            values[IssueInformationKeys.ISSUE], values[IssueInformationKeys.DESCRIPTION]
        )
