from my_assistant.models.credentials import Credentials
from my_assistant.enum import StringEnum
from my_assistant.viewmodels.viewmodel import ViewModel


class CredentialKeys(StringEnum):
    USERNAME = "-USERNAME-"
    PASSWORD = "-PASSWORD-"


class CredentialsViewModel(ViewModel):
    def load(self, result_set) -> Credentials:
        return Credentials(
            result_set[CredentialKeys.USERNAME], result_set[CredentialKeys.PASSWORD]
        )
