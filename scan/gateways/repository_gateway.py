from scan.models import Repository


def create_repositories_in_lot(repositories):
    repositories = [Repository(**repository) for repository in repositories]
    Repository.objects.bulk_create(repositories)
