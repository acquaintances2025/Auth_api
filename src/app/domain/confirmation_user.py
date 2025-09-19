from pydantic import Field

from app.domain import BaseEntity

class ConfirmationUser(BaseEntity):
    code: str = Field(description="Код подтверждений регистрации пользователя")