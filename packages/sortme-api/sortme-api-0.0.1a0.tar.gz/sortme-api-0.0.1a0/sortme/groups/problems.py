import typing
from dataclasses import dataclass
from sortme.group import Group

PREFIX = "/problems"


@dataclass
class Problem:
    name: str

    @dataclass
    class Statement:
        legend: typing.Optional[str]
        input: typing.Optional[str]
        output: typing.Optional[str]
        protocol: typing.Optional[str]
        scoring: typing.Optional[str]
        note: typing.Optional[str]

    statement: Statement

    @dataclass
    class Sample:
        stdin: str
        stdout: str

    samples: list[Sample]

    @dataclass
    class Subtask:
        points: int
        depends: list[int]
        description: str

    subtasks: typing.Optional[list[Subtask]]

    @dataclass
    class Limits:
        time: int
        memory: int

    limits: Limits

    category: int
    difficulty: typing.Optional[int]
    can_edit: bool


class Problems(Group):
    def __init__(self, token, lang):
        super().__init__(token, lang)

    def get_by_id(self, id: int = 0) -> Problem:
        """
        Return general info about user by ID.

        :param id: ID of user. If not provided, get info about current logged-in user.
        """

        return self._make_request("GET", f"{PREFIX}/getByID", {"id": id}, Problem)
