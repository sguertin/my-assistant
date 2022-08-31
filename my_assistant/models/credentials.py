from dataclasses import dataclass


@dataclass(slots=True)
class Credentials:
    username: str
    password: str
