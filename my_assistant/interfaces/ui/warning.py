from abc import abstractmethod, ABCMeta


class IUIWarningService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (
                hasattr(subclass, "warning_ok_cancel_prompt")
                and callable(subclass.warning_ok_cancel_prompt)
            )
            and (
                hasattr(subclass, "warning_prompt")
                and callable(subclass.warning_prompt)
            )
            and (
                hasattr(subclass, "warning_retry_prompt")
                and callable(subclass.warning_retry_prompt)
            )
            or NotImplemented
        )

    @abstractmethod
    def warning_ok_cancel_prompt(self, msg: str):
        """Generates a user prompt with a message and proceed/cancel buttons

        Args:
            msg (str): The message to be displayed

        Returns:
            bool: True if the user selects 'Proceed'
        """
        raise NotImplementedError

    @abstractmethod
    def warning_prompt(self, msg: str):
        """Generates a user prompt with a message and an ok button

        Args:
            msg (str): The message to be displayed
        """
        raise NotImplementedError

    @abstractmethod
    def warning_retry_prompt(self, msg: str) -> bool:
        """Generates a user prompt with a message and retry/cancel buttons

        Args:
            msg (str): The message to be displayed

        Returns:
            bool: True if the user selects 'Retry'
        """
        raise NotImplementedError
