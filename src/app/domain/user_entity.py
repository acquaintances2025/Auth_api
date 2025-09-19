from datetime import datetime

from .base import BaseEntity

class UserModel(BaseEntity):
    id: int
    name: str | None
    lastname: str | None
    surname: str | None
    email: str | None
    number: str | None
    password: str
    age: str | None
    birthday: str | None
    place_birth: str | None
    active: bool | None
    created_at: datetime | None
    block_at: datetime | None