from logging import Logger
from my_assistant.constants import ISSUES_LIST, DELETED_ISSUES_LIST
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.factories.log_factory import ILoggingFactory
from my_assistant.models.issues import Issue


class IssueService(IIssueService):
    log: Logger

    def __init__(self, log_factory: ILoggingFactory):
        self.log = log_factory.get_logger("IssueService")
        if not ISSUES_LIST.exists():
            self.log.info(f"Issues list not found, creating new list")
            with open(ISSUES_LIST, "w") as f:
                f.write("[]")

        if not DELETED_ISSUES_LIST.exists():
            self.log.info(f"Deleted Issues list not found, creating new list")
            with open(DELETED_ISSUES_LIST, "w") as f:
                f.write("[]")

    def get_issues_list(self) -> list[Issue]:
        with open(ISSUES_LIST, "r") as f:
            return Issue.schema().loads(f.read(), many=True)

    def get_deleted_issues(self) -> list[Issue]:
        with open(DELETED_ISSUES_LIST, "r") as f:
            return Issue.schema().loads(f.read(), many=True)

    def save_issues_list(
        self, issues_list: list[Issue], deleted_issues_list: list[Issue] = None
    ):
        with open(ISSUES_LIST, "w") as f:
            f.write(Issue.schema().dumps(issues_list, many=True))

        if deleted_issues_list:
            with open(DELETED_ISSUES_LIST, "w") as f:
                f.write(Issue.schema().dumps(deleted_issues_list, many=True))

    def add_issue(self, issue: Issue) -> "list[Issue]":
        issues_list = self.get_issues_list()
        issues_list.append(issue)
        self.save_issues_list(issues_list)
        return issues_list
