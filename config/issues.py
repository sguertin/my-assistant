from dataclasses import dataclass

from dataclasses_json import dataclass_json

from config.settings import ISSUES_LIST, DELETED_ISSUES_LIST

@dataclass_json
@dataclass
class Issue:
    issue_num: str
    description: str
    disabled: bool = False
    def __str__(self):
        return f'{self.issue_num} - {self.description}'


def get_issues_list() -> list[Issue]:
    with open(ISSUES_LIST, 'r') as f:
        return Issue.schema().loads(f.read(), many=True)

def get_deleted_issues() -> list[Issue]:
    with open(DELETED_ISSUES_LIST, 'r') as f:
        return Issue.schema().loads(f.read(), many=True)

def save_issues_list(issues_list: list[Issue], deleted_issues_list: list[Issue] = None):
    with open(ISSUES_LIST, 'w') as f:
        f.write(Issue.schema().dumps(issues_list, many=True))
    
    if deleted_issues_list:
        with open(DELETED_ISSUES_LIST, 'w') as f:
            f.write(Issue.schema().dumps(deleted_issues_list, many=True))

def add_issue(issue: Issue):
    issues_list = get_issues_list()
    issues_list.append(issue)
    save_issues_list(issues_list)
