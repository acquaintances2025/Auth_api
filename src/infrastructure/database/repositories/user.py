import uuid
import json
from datetime import datetime, date, timedelta

from sqlalchemy import select, or_, insert, and_, update

from ..models.user import TableUserModel
from ..models.confirmation_code import ConfirmationCodeModel
from src.domain import UserModel

from src.infrastructure.database.db.connection import db
from .base import BaseRepository

from typing import Optional

class UserWorks(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)


    async def check_user(self, email: Optional[str], number: Optional[str], name: str, lastname: str, surname: str, birthday: datetime) -> UserModel:
        """Проверка наличия пользователя в базе данных"""
        conditions = []
        conditions.append(TableUserModel.name == name)
        conditions.append(TableUserModel.lastname == lastname)
        conditions.append(TableUserModel.surname == surname)
        conditions.append(TableUserModel.birthday == birthday)
        if email is not None:
            conditions.append(TableUserModel.email == email)
        if number is not None:
            conditions.append(TableUserModel.number == number)

        async with self.session() as session:
            check_user = select(TableUserModel).where(and_(*conditions))
            user = await session.execute(check_user)
            models = user.scalars().all()
            for model in models:
                return await model.to_entity()

    async def create_user(self, uuid_user: uuid.uuid4(), email: Optional[str], number: Optional[str], password: str, name: str, lastname: str, surname: str, birthday: datetime):
        """Создание нового пользователя"""
        async with self.session() as session:
            new_user = insert(TableUserModel).values(
                                                        uuid=str(uuid_user),
                                                        number=number,
                                                        email=email,
                                                        name=name,
                                                        lastname=lastname,
                                                        surname=surname,
                                                        birthday=birthday,
                                                        age= int(date.today().year - birthday.year - ((date.today().month, date.today().day) < (birthday.month, birthday.day))),
                                                        password=password,
                                                        created_at=datetime.now())
            result = await session.execute(new_user)
            await session.commit()
            return result.inserted_primary_key

    async def confirmation_registration(self, uuid_user: str, code: int) -> bool:
        conditions = []
        conditions.append(TableUserModel.uuid == uuid_user)
        conditions.append(ConfirmationCodeModel.code == code)
        conditions.append(ConfirmationCodeModel.active == True)
        async with (self.session() as session):
            check_code = select(ConfirmationCodeModel.active, ConfirmationCodeModel.created_at).join(
                TableUserModel,
                ConfirmationCodeModel.user_id == TableUserModel.id
            ).where(
                and_(*conditions)).distinct()
            users = await session.execute(check_code)
            result = users.mappings().first()
            if result is None:
                return False
            else:
                if result["active"] is True and (datetime.now() - result["created_at"] < timedelta(minutes=10)) is True:
                    update_code =  update(ConfirmationCodeModel).where(ConfirmationCodeModel.code == code).values(active=False)
                    await session.execute(update_code)
                    await session.commit()
                    update_user = update(TableUserModel).where(TableUserModel.uuid == uuid_user).values(active=True)
                    await session.execute(update_user)
                    await session.commit()
                    return True
                else:
                    update_code = update(ConfirmationCodeModel).where(ConfirmationCodeModel.code == code).values(
                        active=False)
                    await session.execute(update_code)
                    await session.commit()
                    return False


