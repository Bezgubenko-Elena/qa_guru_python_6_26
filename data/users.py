from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    user_name: str
    password: str
