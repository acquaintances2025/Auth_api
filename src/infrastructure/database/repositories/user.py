import uuid
import json
from datetime import datetime, date, timedelta


from sqlalchemy import select, or_, insert, and_, update
from starlette.responses import JSONResponse

from ..models.user import TableUserModel
from ..models.token import UserTokenModel
from ..models.confirmation_code import ConfirmationCodeModel
from src.domain import UserModel

from src.infrastructure import verify_password
from src.infrastructure.database.db.connection import db
from .base import BaseRepository

from typing import Optional, Tuple

class UserWorks(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)


    async def check_user(self, email: Optional[str], phone: Optional[str], name: str, lastname: str, surname: str, birthday: datetime) -> UserModel:
        """Проверка наличия пользователя в базе данных"""
        conditions = []
        conditions.append(TableUserModel.name == name)
        conditions.append(TableUserModel.lastname == lastname)
        conditions.append(TableUserModel.surname == surname)
        conditions.append(TableUserModel.birthday == birthday)
        if email is not None:
            conditions.append(TableUserModel.email == email)
        if phone is not None:
            conditions.append(TableUserModel.number == phone)

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
                                                        created_at=datetime.now(),
                                                        role="user")
            result = await session.execute(new_user)
            await session.commit()
            return {"id": result.inserted_primary_key[0], "role": "user"}

    async def confirmation_registration(self, user_id: str, code: int) -> bool:
        conditions = []
        conditions.append(TableUserModel.id == user_id)
        conditions.append(ConfirmationCodeModel.code == code)
        conditions.append(ConfirmationCodeModel.active == True)
        conditions.append(ConfirmationCodeModel.type == "registration")
        async with (self.session() as session):
            check_code = select(ConfirmationCodeModel.active, ConfirmationCodeModel.created_at, ConfirmationCodeModel.type).join(
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
                    update_user = update(TableUserModel).where(TableUserModel.id == user_id).values(active=True)
                    await session.execute(update_user)
                    await session.commit()
                    return True
                else:
                    update_code = update(ConfirmationCodeModel).where(ConfirmationCodeModel.code == code).values(
                        active=False)
                    await session.execute(update_code)
                    await session.commit()
                    return False

    async def authorization_user(self, email: str, phone: str, password: str) -> Tuple[None|dict[str, str], bool]:
        conditions = []
        if email is not None:
            conditions.append(TableUserModel.email == email)
        if phone is not None:
            conditions.append(TableUserModel.number == phone)
        conditions.append(TableUserModel.delete_profile == False)
        async with self.session() as session:
            user_password = select(TableUserModel.password, TableUserModel.id, TableUserModel.role).where(and_(*conditions))
            data_users = await session.execute(user_password)
            result = data_users.mappings().first()
            if result is None:
                return None, False
            if await verify_password(password, result["password"]) is True:
                return {"id": result["id"], "role": result["role"]}, True
            else:
                return None, False

    async def update_user_token(self, user_id: int, access_token: str, refresh_token: str) -> bool:
        async with self.session() as session:
            try:
                token_update = update(UserTokenModel).where(UserTokenModel.user_id == user_id).values(access_token=access_token, refresh_token=refresh_token)
                await session.execute(token_update)
                await session.commit()
                return True
            except Exception as e:
                return False

    async def check_user_in_email_or_phone(self, email: str, phone: str) -> int or None:
        conditions = []
        if email is not None:
            conditions.append(TableUserModel.email == email)
        if phone is not None:
            conditions.append(TableUserModel.number == phone)

        async with self.session() as session:
            check_user = select(TableUserModel.id).where(and_(*conditions))
            user_id = await session.execute(check_user)
            result = user_id.mappings().first()
            if result is not None:
                return result["id"]
            else:
                return None


    async def check_user_in_user_id(self, id: int) -> int or None:
        conditions = []
        if id is not None:
            conditions.append(TableUserModel.id == id)

        async with self.session() as session:
            check_user = select(TableUserModel.email).where(and_(*conditions))
            user_id = await session.execute(check_user)
            result = user_id.mappings().first()
            if result is not None:
                return result["email"]
            else:
                return None

    async def check_user_code_in_user_id(self, user_id: int, code: int) -> Tuple[bool, str|None]:
        async with self.session() as session:

            user_time_code = select(ConfirmationCodeModel.created_at).where(and_(
                                                                                ConfirmationCodeModel.user_id == user_id,
                                                                                ConfirmationCodeModel.code == code,
                                                                                ConfirmationCodeModel.active == True,
                                                                                ConfirmationCodeModel.type == "password_recovery"
                                                                            )
                                                                        )
            user_time = await session.execute(user_time_code)
            result = user_time.mappings().first()
            if result is not None:
                if (datetime.now() - result["created_at"] < timedelta(minutes=10)) is True:
                    update_active = update(ConfirmationCodeModel).where(and_(ConfirmationCodeModel.user_id == user_id, ConfirmationCodeModel.code == code)).values(active=False)
                    await session.execute(update_active)
                    await session.commit()
                    return True, None
                else:
                    update_active = update(ConfirmationCodeModel).where(ConfirmationCodeModel.user_id == user_id and ConfirmationCodeModel.code == code).values(active=False)
                    await session.execute(update_active)
                    await session.commit()
                    return False, "Код подтверждения устарел."
            else:
                return False, "Код подтверждения не найден."

    async def update_password(self, password: str, user_id: int) -> Tuple[bool, str]:
        try:
            async with self.session() as session:
                update_password = update(TableUserModel).where(
                    TableUserModel.id == user_id).values(password=password)
                await session.execute(update_password)
                await session.commit()
                return True, "Пароль успешно обновлен."
        except Exception as e:
            return False, "В процессе обновления произошла ошибка."

    async def user_id_in_refresh(self, refresh_token):
        async with self.session() as session:
            get_user_id = select(UserTokenModel.user_id).where(UserTokenModel.refresh_token == refresh_token)
            user_id = await session.execute(get_user_id)
            result = user_id.mappings().first()
            if result is not None:
                return result["user_id"]


