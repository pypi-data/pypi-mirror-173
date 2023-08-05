import requests


class ForbiddenError(requests.HTTPError):
    pass


class TooManyRequestsError(requests.HTTPError):
    pass


class NotFoundError(requests.HTTPError):
    pass


class APIError(requests.HTTPError):
    pass