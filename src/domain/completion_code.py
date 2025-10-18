from pydantic import Field

from src.domain import BaseEntity

class CompletionCode(BaseEntity):
    user_id: int = Field(description="Id пользователя пользователя")
    phone: str|None = Field(default=None, description="Номер телефона пользователя")
    email: str|None = Field(default=None, description="Email пользователя")
    code: int = Field(description="Код подтверждений email/номера телефона пользователя")