import dacite
import datetime
from typing import Type, Dict, Union, TypeVar
from .errors import *

HOSTNAME = "https://api.sort-me.org"

T = TypeVar("T")
dacite_config = dacite.Config(type_hooks={
    datetime.datetime: lambda x: datetime.datetime.fromtimestamp(x),
    tuple[int, int, int, int, int]: lambda x: tuple(x)
})


class Group:
    def __init__(self, token: str = None, lang: str = "ru"):
        self._token = token
        self._lang = lang

    def _make_request(self, method: str, path: str, params: Dict[str, Union[str, int, list[str, int]]],
                      data_class: Type[T] = None) -> T:

        if "lang" not in params:
            params["lang"] = self._lang

        headers = {"X-client": "python-api"}
        if self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"

        params = "?" + "&".join(f"{k}={v}" for k, v in params.items())

        r = requests.request(method, f"{HOSTNAME}{path}{params if params != '?' else ''}", headers=headers)

        match r.status_code:
            case 200 | 201:
                if data_class is not None:
                    return dacite.from_dict(data_class, r.json(), config=dacite_config)
                else:
                    return r.json()
            case 403:
                raise ForbiddenError(r.reason)

            case 404:
                raise NotFoundError()

            case 429:
                raise TooManyRequestsError()
            case _:
                try:
                    body = r.json()
                except requests.exceptions.JSONDecodeError:
                    r.raise_for_status()
                else:
                    if 'error' in body:
                        raise APIError(body["error"])
