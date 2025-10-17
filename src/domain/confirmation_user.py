from pydantic import Field

from .base import BaseEntity

class ConfirmationUser(BaseEntity):
    code: int = Field(description="Код подтверждений регистрации пользователя")