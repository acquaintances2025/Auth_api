from datetime import datetime

from .base import BaseEntity

class CodeModel(BaseEntity):
    id: int
    user_id: int
    code: int
    created_at: datetime