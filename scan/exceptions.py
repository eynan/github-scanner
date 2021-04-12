
class GithubException(Exception):
    def __init__(self, code: int, reason: str, detail: str):
        message = f'Github api returned the status code {code}, reason: {reason}, detail: {detail}.'
        super(GithubException, self).__init__(message)
