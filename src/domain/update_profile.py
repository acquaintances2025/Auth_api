from pydantic import Field
from .base import BaseEntity

from datetime import datetime
from typing import List

class UpdateProfile(BaseEntity):
    name: str|None = Field(default=None, description='Имя пользователя')
    surname: str|None = Field(default=None, description='Фамилия пользователя')
    lastname: str|None = Field(default=None, description='Отчество пользователя')
    birthday: datetime|None = Field(default=None, description='Дата рождения')
    place_birth: str|None = Field(default=None, description="Место рождения")
    number: str|None = Field(default=None, description='Номер телефона')
    email: str|None = Field(default=None, description='Email пользователя')
