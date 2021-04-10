from typing import List

from scan.models import User
from scan.types import User as UserType


def get_last_user_id_created() -> int:
    users = list(User.objects.filter().order_by('-id')[:1])
    if users:
        return users[0].id
    return 0


def create_users_in_lot(users: List[UserType]) -> None:
    users = [User(**user) for user in users]
    User.objects.bulk_create(users)
