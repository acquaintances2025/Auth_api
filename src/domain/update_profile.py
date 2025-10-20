from pydantic import Field
from datetime import datetime


from .base import BaseEntity

class UpdateProfile(BaseEntity):
    user_id: int = Field(description="Id пользователя")
    name: str|None = Field(default=None, description='Имя пользователя')
    surname: str|None = Field(default=None, description='Фамилия пользователя')
    lastname: str|None = Field(default=None, description='Отчество пользователя')
    birthday: datetime|None = Field(default=None, description='Дата рождения')
    place_birth: str|None = Field(default=None, description="Место рождения")
