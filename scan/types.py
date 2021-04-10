from datetime import datetime
from typing import TypedDict, Optional


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
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    pushed_at: Optional[datetime]
    language: str
    forks_count: int
    stargazers_count: int
    watchers_count: int
