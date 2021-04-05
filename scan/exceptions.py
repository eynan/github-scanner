
class GithubException(Exception):
    def __init__(self, code, reason):
        message = f'Github api returned the status code {code}, reason: {reason}.'
        super(GithubException, self).__init__(message)
