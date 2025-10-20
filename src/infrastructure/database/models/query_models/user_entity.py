from datetime import datetime

from src.domain import BaseEntity

class UserModel(BaseEntity):
    id: int
    name: str | None
    lastname: str | None
    surname: str | None
    email: str | None
    number: str | None
    password: str
    age: int | None
    birthday: datetime | None
    active: bool
    created_at: datetime | None
    block_at: datetime | None
    active_phone: bool
    active_email: bool
    place_birth: str | None
    delete_profile: bool | None
    delete_profile_at: datetime | None

