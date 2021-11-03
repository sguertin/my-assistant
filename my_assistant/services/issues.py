from my_assistant.constants import ISSUES_LIST, DELETED_ISSUES_LIST
from my_assistant.events import ADD_EVENT, ANOTHER_EVENT, CLOSE_EVENT, REMOVE_EVENT, RESTORE_EVENT, SAVE_EVENT, CLOSE_EVENTS, SAVE_EVENTS
from my_assistant.interfaces.ui import IUIProvider
from my_assistant.models.issues import Issue


class IssueService:
    ui_provider: IUIProvider

    def __init__(self, ui_provider: IUIProvider):
        self.ui_provider = ui_provider
        ui_provider.warning_retry_prompt()

    def get_all_issues(self) -> tuple[list[Issue], list[Issue]]:
        return self.get_active_issues(), self.get_deleted_issues()

    def get_active_issues(self) -> list[Issue]:
        with open(ISSUES_LIST, 'r') as f:
            return Issue.schema().loads(f.read(), many=True)

    def get_deleted_issues(self) -> list[Issue]:
        with open(DELETED_ISSUES_LIST, 'r') as f:
            return Issue.schema().loads(f.read(), many=True)

    def save_issues_list(self, issues_list: list[Issue], deleted_issues_list: list[Issue] = None):
        with open(ISSUES_LIST, 'w') as f:
            f.write(Issue.schema().dumps(issues_list, many=True))

        if deleted_issues_list:
            with open(DELETED_ISSUES_LIST, 'w') as f:
                f.write(Issue.schema().dumps(deleted_issues_list, many=True))

    def manage_issues(self) -> list[Issue]:
        issues, deleted_issues = self.get_all_issues()
        return self.ui_provider.manage_issues(
            issues, deleted_issues, self.handle_issue_list_events)

    def add_issue(self, issue: Issue) -> list[Issue]:
        issues_list = self.get_active_issues()
        issues_list.append(issue)
        self.save_issues_list(issues_list)
        return issues_list

    def handle_issue_list_events(self, event: str, active_issues: list[Issue], deleted_issues: list[Issue]) -> tuple[list[Issue], list[Issue]]:
        issues, deleted_issues = self.get_all_issues()
        if event == ADD_EVENT:
            self.ui_provider.get_issue_info(self.handle_add_issue_events)
            issues = self.get_active_issues()
            has_changes = True
        elif event == REMOVE_EVENT:
            for issue in active_issues:
                issues.remove(issue)
                deleted_issues.append(issue)
            has_changes = True
        elif event == RESTORE_EVENT:
            for issue in deleted_issues:
                deleted_issues.remove(issue)
                issues.append(issue)
            has_changes = True
        if event == SAVE_EVENT:
            self.save_issues_list(issues, deleted_issues)
        if event in CLOSE_EVENTS and has_changes:
            proceed = self.ui_provider.warning_ok_cancel_prompt(
                'None of your changes have been saved, are you sure want to continue?')
            if proceed:
                return False, False
        return issues, deleted_issues

    def handle_add_issue_events(self, event: str, issue_num: str, description: str) -> str:
        issues = self.get_active_issues()
        if event in SAVE_EVENTS:
            if issue_num:
                if issue_num not in issues:
                    issue = Issue(issue_num, description)
                    self.add_issue(issue)
                    if event == SAVE_EVENT:
                        return CLOSE_EVENT
                    elif event == ANOTHER_EVENT:
                        return f'Issue {issue_num} was successfully added'
                return f'ERROR: Issue {issue_num} already exists'
            return f'ERROR: Issue number is required'
