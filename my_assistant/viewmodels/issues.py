from enum import Enum

from my_assistant.models.issues import Issue
from my_assistant.viewmodels.viewmodel import ViewModel


class IssueInformationKeys(Enum):
    ISSUE = "-ISSUE-"
    DESCRIPTION = "-DESCRIPTION-"
    RESULT = "-RESULT-"


class IssueInformationViewModel(ViewModel):
    issue: Issue
    result_text: str
    def load(self, values: dict[str, str]) -> "IssueInformationViewModel":
        self.result_text = values[IssueInformationKeys.RESULT]
        self.issue = Issue(
            values[IssueInformationKeys.ISSUE], values[IssueInformationKeys.DESCRIPTION]
        )
        return self
