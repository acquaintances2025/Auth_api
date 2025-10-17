from datetime import datetime

from src.domain.base import BaseEntity


class TokenModel(BaseEntity):
    id: int
    access_token: str
    refresh_token: str
    created_at: datetime | None
