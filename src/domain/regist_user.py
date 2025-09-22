from pydantic import Field

from datetime import datetime
from src.domain import BaseEntity

class RegistrationUser(BaseEntity):
    number: str | None = Field(default=None, description="Номер телефона пользователя")
    name: str = Field(description="Имя пользователя")
    lastname: str = Field(description="Фамилия пользователя")
    surname: str = Field(description="Отчество пользователя")
    birthday: datetime = Field(description="Дата рождения")
    email: str | None = Field(default=None, description="Email пользователя")
    password: str = Field(description="Пароль пользователя")
    confirm_password: str = Field(description="Подтверждение пароля пользователя")

