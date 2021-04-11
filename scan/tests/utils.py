from django.utils import timezone


class HttpResponseFake:
    def __init__(self, status_code=None, content=None, reason=None, headers=None):
        self.content = content
        self.status_code = status_code
        self.reason = reason
        self.headers = headers


def get_repository_struct(id, user_id):
    return {
        'id': id,
        'user_id': user_id,
        'description': 'test',
        'name': 'test',
        'full_name': 'test',
        'created_at': timezone.now().replace(microsecond=0),
        'updated_at': timezone.now().replace(microsecond=0),
        'pushed_at': timezone.now().replace(microsecond=0),
        'language': 'test',
        'forks_count': 2,
        'stargazers_count': 2,
        'watchers_count': 2
    }
