from my_assistant.interfaces.base import Interface


class IAuthenticationProvider(Interface):
    """interface for an authentication provider for storing and returning credentials
    """

    def clear_auth(self) -> None:
        """Clears the current authentication token
        """

    def get_auth(self) -> str:
        """Returns the authentication credentials

        Returns:
            str: authentication token
        """
        pass

    def set_auth(self, user_name: str, password: str):
        """Set authorization token

        Args:
            user_name (str): The user name
            password (str): the user's password
        """
        pass
