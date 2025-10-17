from pydantic import Field

from .base import BaseEntity

class ConfirmationEmail(BaseEntity):
    user_id: int = Field(description="Код подтверждений регистрации пользователя")
    email: str = Field(description="Email пользователя")
