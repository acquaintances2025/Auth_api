import uuid
from datetime import datetime

from sqlalchemy import select, or_, insert

from ..models.user import CallMetaInfoModel
from app.domain import UserModel

from app.infrastructure.database.db.connection import db
from .base import BaseRepository

from typing import Optional

class UserWorks(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)


    async def check_user(self, email: Optional[str], number: Optional[str]) -> UserModel:
        """Проверка наличия пользователя в базе данных"""
        conditions = []
        if email is not None:
            conditions.append(CallMetaInfoModel.email == email)
        if number is not None:
            conditions.append(CallMetaInfoModel.number == number)

        async with self.session() as session:
            check_user = select(CallMetaInfoModel).where(or_(*conditions))
            user = await session.execute(check_user)
            models = user.scalars().all()
            for model in models:
                return await model.to_entity()

    async def create_user(self, uuid_user: uuid.uuid4(), email: Optional[str], number: Optional[str], password: str):
        """Создание нового пользователя"""
        async with self.session() as session:
            new_user = insert(CallMetaInfoModel).values(
                                                        uuid=str(uuid_user),
                                                        number=number,
                                                        email=email,
                                                        password=password,
                                                        created_at=datetime.now())
            result = await session.execute(new_user)
            await session.commit()
            return result.inserted_primary_key
