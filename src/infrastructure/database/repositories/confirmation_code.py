from sqlalchemy import select, or_, insert
from datetime import datetime


from src.infrastructure.database.db.connection import db
from ..models.confirmation_code import ConfirmationCodeModel

from .base import BaseRepository

class CodeWorks(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)

    async def create_confirmation_code(self, user_id: int, confirmation_code: int) -> None:
        async with self.session() as session:
            add_user_code = insert(ConfirmationCodeModel).values(user_id=user_id, code=confirmation_code, created_at=datetime.now())
            await session.execute(add_user_code)
            await session.commit()