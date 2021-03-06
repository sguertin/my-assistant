import base64

from my_assistant.providers.interfaces.authentication import IAuthenticationProvider


class BasicAuthenticationProvider(IAuthenticationProvider):
    _auth: bytes = None

    def clear_auth(self) -> None:
        self._auth = None

    def get_auth(self) -> str:
        if self._auth is not None:
            return f"Basic {self._auth.decode()}"
        return None

    def set_auth(self, user_name: str, password: str):
        encoding = base64.b64encode(f"{user_name}:{password}".encode("utf-8"))
        self._auth = encoding
