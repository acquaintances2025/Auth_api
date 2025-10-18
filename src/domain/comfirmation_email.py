from pydantic import Field

from .base import BaseEntity

class ConfirmationEmail(BaseEntity):
    user_id: int = Field(description="Id пользователя пользователя")
    email: str = Field(description="Email пользователя")
