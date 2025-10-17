from sqlalchemy import select, or_, insert


from src.infrastructure.database.db.connection import db
from ..models.token import UserTokenModel


from .base import BaseRepository

class TokenWorks(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)


    async def create_token(self, user_id:int, access_token: str, refresh_token: str) -> None:
        async with self.session() as session:
            add_user_token = insert(UserTokenModel).values(
                                                            user_id=user_id,
                                                            access_token=access_token,
                                                            refresh_token=refresh_token
                                                        )
            await session.execute(add_user_token)
            await session.commit()