import base64

from my_assistant.interfaces.authentication import IAuthenticationProvider


class BasicAuthenticationProvider(IAuthenticationProvider):
    _auth: bytes

    def __init__(self: IAuthenticationProvider):
        self._auth = None

    def clear_auth(self: IAuthenticationProvider) -> None:
        self._auth = None

    def get_auth(self: IAuthenticationProvider) -> str:
        if self._auth is not None:
            return f'Basic {self._auth.decode()}'
        return None

    def set_auth(self: IAuthenticationProvider, user_name: str, password: str):
        encoding = base64.b64encode(f'{user_name}:{password}'.encode('utf-8'))
        self._auth = encoding
