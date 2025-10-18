from pydantic import Field

from .base import BaseEntity

class ConfirmationPhone(BaseEntity):
    user_id: int = Field(description="Код подтверждений регистрации пользователя")
    phone: str = Field(description="Номер телефона пользователя")