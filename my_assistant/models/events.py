from enum import Enum


class Events(Enum):
    ANOTHER = "Another"
    CANCEL = "Cancel"
    CLOSE = "Close"
    CONTINUE = "Continue"
    OK = "Ok"
    RETRY = "Retry"
    SAVE = "Save"
    SUBMIT = "Submit"

    def __repr__(self):
        return str(self)
