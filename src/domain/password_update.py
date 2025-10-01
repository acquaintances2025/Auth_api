from pydantic import Field

from .base import BaseEntity

class PasswordUpdate(BaseEntity):
    user_id: int = Field(description="Id пользователя")
    code: int = Field(description="Код подтверждения смены пароля")
    password: str = Field(description="Новый пароль пользователя")
    confirm_password: str = Field(description="Подтверждение нового пароля пользователя")