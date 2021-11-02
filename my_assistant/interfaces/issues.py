from my_assistant.models.issues import Issue


class IIssueService:

    def __init__(self, *args):
        raise TypeError('Interface IIssueService cannot be initialized')

    def get_all_issues(self) -> tuple[list[Issue], list[Issue]]:
        raise NotImplementedError('get_all_issues is not implemented')

    def get_issues_list(self) -> list[Issue]:
        raise NotImplementedError('get_issues_list is not implemented')

    def get_deleted_issues(self) -> list[Issue]:
        raise NotImplementedError('get_deleted_issues is not implemented')

    def manage_issues(self) -> list[Issue]:
        raise NotImplementedError('manage_issues is not implemented')

    def save_issues_list(self, issues_list: list[Issue], deleted_issues_list: list[Issue] = None):
        raise NotImplementedError('save_issues_list is not implemented')

    def add_issue(self, issue: Issue) -> 'list[Issue]':
        raise NotImplementedError('add_issue is not implemented')
