import json
from datetime import datetime
from http import HTTPStatus
from time import time, sleep
from typing import List

import requests
import asyncio

from aiohttp import ClientSession

from scan.exceptions import GithubException
from scan.types import User, Repository

MAXIMUM_RECORDS_GITHUB_RETURN = 100
DATE_FORMAT_GITHUB = '%Y-%m-%dT%H:%M:%S%z'


def fetch_github_users_greater_then_the_last_user_id(last_user_id: int, records_per_page: int = 30) -> List[User]:
    url_users = f'https://api.github.com/users'
    params = {
        'accept': 'application/vnd.github.v3+json',
        'since': last_user_id,
        'per_page': records_per_page
    }

    response = requests.get(url_users, params=params)

    if response.status_code == HTTPStatus.OK:
        return [parse_github_user_to_user(github_user) for github_user in json.loads(response.content)]

    elif response.status_code == HTTPStatus.FORBIDDEN and response.reason == 'rate limit exceeded':
        time_to_reset = int(response.headers['X-RateLimit-Reset'])
        seconds_to_wait = time_to_reset - time()
        if seconds_to_wait > 0:
            sleep(seconds_to_wait)
        return fetch_github_users_greater_then_the_last_user_id(last_user_id)

    else:
        raise GithubException(response.status_code, response.reason)


async def fetch_login_repository(session: ClientSession, login: str, page: int = 1) -> List[Repository]:
    params = {
        'accept': 'application/vnd.github.v3+json',
        'per_page': MAXIMUM_RECORDS_GITHUB_RETURN,
        'page': page,
        'type': 'owner'
    }
    async with session.get(f'https://api.github.com/users/{login}/repos', params=params) as response:
        status_code = response.status
        repositories = []
        if status_code == HTTPStatus.OK:
            repositories = await response.json()
            if 'next' in response.headers.get('Link', ''):
                provisional_result = await fetch_login_repository(session, login, page + 1)
                repositories.extend(provisional_result)
        elif status_code == HTTPStatus.FORBIDDEN:
            seconds_to_reset = int(response.headers['X-RateLimit-Reset'])
            seconds_to_wait = seconds_to_reset - time()
            if seconds_to_wait > 0:
                await asyncio.sleep(seconds_to_wait)
            return await fetch_login_repository(session, login, page)
        else:
            raise GithubException(status_code, response.reason)
        return [parse_github_repository_to_repository(repository) for repository in repositories] if page == 1 else repositories


def parse_github_user_to_user(github_user: dict) -> User:
    return {
        'id': github_user['id'],
        'login': github_user['login'],
        'url': github_user['url']
    }


def parse_github_repository_to_repository(github_repository: dict) -> Repository:
    return {
        'id': github_repository['id'],
        'user_id': github_repository['owner']['id'],
        'description': github_repository['description'],
        'name': github_repository['name'],
        'full_name': github_repository['full_name'],
        'created_at': datetime.strptime(github_repository['created_at'], DATE_FORMAT_GITHUB) if github_repository['created_at'] else None,
        'updated_at': datetime.strptime(github_repository['updated_at'], DATE_FORMAT_GITHUB) if github_repository['updated_at'] else None,
        'pushed_at': datetime.strptime(github_repository['pushed_at'], DATE_FORMAT_GITHUB) if github_repository['pushed_at'] else None,
        'language': github_repository['language'],
        'forks_count': github_repository['forks_count'],
        'stargazers_count': github_repository['stargazers_count'],
        'watchers_count': github_repository['watchers_count']
    }
