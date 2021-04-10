class HttpResponseFake:
    def __init__(self, status_code=None, content=None, reason=None, headers=None):
        self.content = content
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
