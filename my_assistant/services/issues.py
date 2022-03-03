from my_assistant.constants import ISSUES_LIST, DELETED_ISSUES_LIST
from my_assistant.models.issues import Issue


class IssueService:

    def get_issues_list(self) -> 'list[Issue]':
        with open(ISSUES_LIST, 'r') as f:
            return Issue.schema().loads(f.read(), many=True)

    def get_deleted_issues(self) -> 'list[Issue]':
        with open(DELETED_ISSUES_LIST, 'r') as f:
            return Issue.schema().loads(f.read(), many=True)

    def save_issues_list(self, issues_list: 'list[Issue]', deleted_issues_list: 'list[Issue]' = None):
        with open(ISSUES_LIST, 'w') as f:
            f.write(Issue.schema().dumps(issues_list, many=True))

        if deleted_issues_list:
            with open(DELETED_ISSUES_LIST, 'w') as f:
                f.write(Issue.schema().dumps(deleted_issues_list, many=True))

    def add_issue(self, issue: Issue) -> 'list[Issue]':
        issues_list = get_issues_list()
        issues_list.append(issue)
        self.save_issues_list(issues_list)
        return issues_list


def get_issues_list() -> 'list[Issue]':
    with open(ISSUES_LIST, 'r') as f:
        return Issue.schema().loads(f.read(), many=True)


def get_deleted_issues() -> 'list[Issue]':
    with open(DELETED_ISSUES_LIST, 'r') as f:
        return Issue.schema().loads(f.read(), many=True)


def save_issues_list(issues_list: 'list[Issue]', deleted_issues_list: 'list[Issue]' = None):
    with open(ISSUES_LIST, 'w') as f:
        f.write(Issue.schema().dumps(issues_list, many=True))

    if deleted_issues_list:
        with open(DELETED_ISSUES_LIST, 'w') as f:
            f.write(Issue.schema().dumps(deleted_issues_list, many=True))


def add_issue(issue: Issue) -> 'list[Issue]':
    issues_list = get_issues_list()
    issues_list.append(issue)
    save_issues_list(issues_list)
    return issues_list
