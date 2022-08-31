from my_assistant.models.credentials import Credentials
from my_assistant.enum import StringEnum
from my_assistant.viewmodels.viewmodel import ViewModel


class CredentialKeys(StringEnum):
    USERNAME = "-USERNAME-"
    PASSWORD = "-PASSWORD-"


class CredentialsViewModel(ViewModel):
    credentials: Credentials
    def load(self, result_set) -> "CredentialsViewModel":
        self.credentials = Credentials(
            result_set[CredentialKeys.USERNAME], result_set[CredentialKeys.PASSWORD]
        )
        return self
