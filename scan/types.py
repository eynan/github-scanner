from datetime import datetime
from typing import TypedDict


class User(TypedDict):
    id: int
    login: str
    url: str


class Repository(TypedDict):
    id: int
    user_id: int
    description: str
    name: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    language: str
    forks_count: int
    stargazers_count: int
    watchers_count: int
