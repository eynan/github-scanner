from typing import List

import aiohttp
import asyncio

from scan.exceptions import GithubException
from scan.gateways.github_gateway import fetch_github_users_greater_then_the_last_user_id, fetch_login_repository
from scan.gateways.repository_gateway import create_repositories_in_lot
from scan.gateways.user_gateway import get_last_user_id_created, create_users_in_lot
from scan.log import create_log_error


def screap_users_and_repositories_data_from_github():
    last_user_id_created = get_last_user_id_created()
    users = fetch_github_users_greater_then_the_last_user_id(last_user_id_created)
    create_users_in_lot(users)
    logins = [user['login'] for user in users]
    repositories_collection = asyncio.run(screap_repositories_date_from_users_logins_async(logins), debug=True)
    for repository in repositories_collection:
        if isinstance(repository, GithubException):
            create_log_error(repository)
        else:
            create_repositories_in_lot(repository)


async def screap_repositories_date_from_users_logins_async(users_logins: List[str]) -> any:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for login in users_logins:
            task = asyncio.create_task(fetch_login_repository(session, login))
            tasks.append(task)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


