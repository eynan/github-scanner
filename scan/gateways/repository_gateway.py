from typing import List

from scan.models import Repository
from scan.types import Repository as RepositoryType


def create_repositories_in_lot(repositories: List[RepositoryType]) -> None:
    repositories = [Repository(**repository) for repository in repositories]
    Repository.objects.bulk_create(repositories)
