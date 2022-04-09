from abc import abstractmethod, ABCMeta


class IUICredentialsService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "credentials_prompt")
            and callable(subclass.credentials_prompt)
        ) or NotImplemented

    @abstractmethod
    def credentials_prompt(self) -> tuple[str, str]:
        """Generates a user prompt asking for a user name and raise NotImplementedErrorword

        Returns:
            tuple[str, str]: the username and raise NotImplementedErrorword
        """
        raise NotImplementedError()
