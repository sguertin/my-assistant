from abc import ABCMeta, abstractmethod


class IAuthenticationProvider(metaclass=ABCMeta):
    """interface for an authentication provider for storing and returning credentials"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "clear_auth") and callable(subclass.clear_auth))
            and (hasattr(subclass, "get_auth") and callable(subclass.get_auth))
            and (hasattr(subclass, "set_auth") and callable(subclass.set_auth))
            or NotImplemented
        )

    @abstractmethod
    def clear_auth(self) -> None:
        """Clears the current authentication token"""
        raise NotImplementedError

    @abstractmethod
    def get_auth(self) -> str:
        """Returns the authentication credentials

        Returns:
            str: authentication token
        """
        raise NotImplementedError

    @abstractmethod
    def set_auth(self, user_name: str, password: str):
        """Set authorization token

        Args:
            user_name (str): The user name
            password (str): the user's password
        """
        raise NotImplementedError
