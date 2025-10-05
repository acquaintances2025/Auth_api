from src.infrastructure.database.db.connection import db
from .base import BaseRepository

from datetime import datetime
from pydantic import BaseModel

from sqlalchemy import select

from ..models.user import TableUserModel

from typing import Optional, Tuple

class UserProfile(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)


    async def user_profile(self, user_id):

        class Profile(BaseModel):
            name: str
            surname: str
            lastname: str
            email: str|None
            number: str|None
            age: int
            birthday: datetime
            created_at: datetime
            active_phone: bool
            active_email: bool
            active: bool

        async with self.session() as session:
            get_profiles = select(TableUserModel.name,
                                  TableUserModel.surname,
                                  TableUserModel.lastname,
                                  TableUserModel.email,
                                  TableUserModel.number,
                                  TableUserModel.age,
                                  TableUserModel.birthday,
                                  TableUserModel.active,
                                  TableUserModel.created_at,
                                  TableUserModel.active_phone,
                                  TableUserModel.active_email).where(TableUserModel.id == user_id).limit(1)
            profile = await session.execute(get_profiles)
            answer = profile.mappings().first()
            if answer is not None:
                return Profile(**answer)
            else:
                return None
