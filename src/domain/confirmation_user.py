from pydantic import Field

from src.domain import BaseEntity

class ConfirmationUser(BaseEntity):
    code: int = Field(description="Код подтверждений регистрации пользователя")