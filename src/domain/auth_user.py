from pydantic import Field

from src.domain import BaseEntity


class AuthUser(BaseEntity):
    number: str = Field(default=None, description="Номер телефона пользователя")
    email: str = Field(default=None, description="Email пользователя")
    password: str = Field(description="Пароль пользователя")