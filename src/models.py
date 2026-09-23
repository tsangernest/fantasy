import functools
import datetime
import uuid
import typing

from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    uuid: uuid.UUID = Field(default_factory=uuid.uuid7, primary_key=True)
    espn_id: int = Field(nullable=False)

    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    dob: datetime.date = Field(unique=False, nullable=False)

    @functools.cached_property
    def display_name(self) -> str:
        first = f"{self.first_name[0].capitalize()}{self.first_name[1:]}"
        last = f"{self.last_name[0].capitalize()}{self.last_name[1:]}"
        return f"{first} {last}"

    @functools.cached_property
    def age(self) -> int:
        today = datetime.date.today()
        birthday_not_passed = (today.month, today.day) < (self.dob.month, self.dob.day)
        return today.year - self.dob.year - birthday_not_passed


class Team(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    espn_id: int = Field(nullable=False)

    display_name: str = Field(nullable=False)
    abbreviation: str = Field(max_length=3, nullable=False)
    # name: str = Field(nullable=False)

