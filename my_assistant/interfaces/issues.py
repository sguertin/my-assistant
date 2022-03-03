from my_assistant.interfaces.base import Interface
from my_assistant.models.issues import Issue


class IIssueService(Interface):

    def get_issues_list(self) -> 'list[Issue]':
        pass

    def get_deleted_issues(self) -> 'list[Issue]':
        pass

    def save_issues_list(self, issues_list: 'list[Issue]', deleted_issues_list: 'list[Issue]' = None):
        pass

    def add_issue(self, issue: Issue) -> 'list[Issue]':
        pass
