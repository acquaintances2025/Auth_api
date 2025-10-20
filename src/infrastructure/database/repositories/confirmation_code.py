from sqlalchemy import insert, select, and_, update
from datetime import datetime

from .base import BaseRepository
from ..db.connection import db
from ..models.table_models.confirmation_code import ConfirmationCodeModel
from ..models.table_models.user import TableUserModel

class CodeWorks(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)

    async def create_confirmation_code(self, user_id: int, confirmation_code: int, types: str) -> None:
        async with self.session() as session:
            add_user_code = insert(ConfirmationCodeModel).values(user_id=user_id, code=confirmation_code, created_at=datetime.now(), type=types)
            await session.execute(add_user_code)
            await session.commit()

    async def check_confirmation_code(self, user_id: int, confirmation_code: int) -> bool:
        conditions = []
        conditions.append(ConfirmationCodeModel.user_id == user_id)
        conditions.append(ConfirmationCodeModel.code == confirmation_code)
        conditions.append(ConfirmationCodeModel.active == True)
        async with (self.session() as session):
            check_code = select(ConfirmationCodeModel.active, ConfirmationCodeModel.created_at,
                                ConfirmationCodeModel.type).where(and_(*conditions)).distinct()
            users = await session.execute(check_code)
            result = users.mappings().first()
            return result

    async def blok_confirmation_code(self, user_id: int, confirmation_code: int) -> None:
        conditions = []
        conditions.append(ConfirmationCodeModel.user_id == user_id)
        conditions.append(ConfirmationCodeModel.code == confirmation_code)
        conditions.append(ConfirmationCodeModel.active == True)
        async with (self.session() as session):
            update_code = update(ConfirmationCodeModel).where(and_(*conditions)).values(active=False)
            await session.execute(update_code)
            await session.commit()

    async def check_registration_code(self, user_id, confirmation_code: int) -> bool:
        conditions = []
        conditions.append(TableUserModel.id == user_id)
        conditions.append(ConfirmationCodeModel.code == confirmation_code)
        conditions.append(ConfirmationCodeModel.active == True)
        conditions.append(ConfirmationCodeModel.type == "registration")
        async with (self.session() as session):
            check_code = select(ConfirmationCodeModel.active, ConfirmationCodeModel.created_at,
                                ConfirmationCodeModel.type).join(
                TableUserModel,
                ConfirmationCodeModel.user_id == TableUserModel.id
            ).where(
                and_(*conditions)).distinct()
            users = await session.execute(check_code)
            result = users.mappings().first()
            return result