from abc import ABCMeta, abstractmethod
from my_assistant.models.issues import Issue


class IIssueService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (
                hasattr(subclass, "get_issues_list")
                and callable(subclass.get_issues_list)
            )
            and (
                hasattr(subclass, "get_deleted_issues")
                and callable(subclass.get_deleted_issues)
            )
            and (
                hasattr(subclass, "save_issues_list")
                and callable(subclass.save_issues_list)
            )
            and (hasattr(subclass, "add_issue") and callable(subclass.add_issue))
            or NotImplemented
        )

    @abstractmethod
    def get_issues_list(self) -> list[Issue]:
        """Retrieves the list of active issues to log hours against

        Returns:
            list[Issue]: The list of active issues
        """
        raise NotImplementedError()

    @abstractmethod
    def get_deleted_issues(self) -> list[Issue]:
        """Retrieves the list of issues deleted from the active list

        Returns:
            list[Issue]: The list of deleted issues
        """
        raise NotImplementedError()

    @abstractmethod
    def save_issues_list(
        self, issues_list: list[Issue], deleted_issues_list: list[Issue] = None
    ) -> None:
        """Save the updated issue list and, optionally, the deleted list of issues

        Args:
            issues_list (list[Issue]): The current active issues list
            deleted_issues_list (list[Issue], optional): The list of deleted issues. Defaults to None.

        """
        raise NotImplementedError()

    @abstractmethod
    def add_issue(self, issue: Issue) -> list[Issue]:
        """Add a new issue to the list of active issues

        Args:
            issue (Issue): The new active issue

        Returns:
            list[Issue]: The new list of active issues
        """
        raise NotImplementedError()
