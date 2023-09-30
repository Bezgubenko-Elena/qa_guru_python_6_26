from dataclasses import dataclass


@dataclass
class User:
    user_name: str
    password: str


@dataclass
class Book:
    title: str
    ISBN: str
