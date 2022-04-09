from abc import abstractmethod, ABCMeta

from my_assistant.models.issues import Issue


class IUIIssueService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "get_issue_info") and callable(subclass.get_issue_info))
            and (
                hasattr(subclass, "manage_issues") and callable(subclass.manage_issues)
            )
            or NotImplemented
        )

    @abstractmethod
    def get_issue_info(self, issues: list[Issue]) -> list[Issue]:
        """Creates UI control to capture issue information and add to list

        Args:
            issues (list[Issue]): The current list of issues

        Returns:

        """
        raise NotImplementedError()

    @abstractmethod
    def manage_issues(self) -> tuple[bool, list[Issue]]:
        """Generates a UI Prompt to allow the user to add and remove issues from the list available

        Returns:
            tuple[bool, list[Issue]]: a tuple, True if the user selected 'Save', and the updated list of issues
        """
        raise NotImplementedError()
