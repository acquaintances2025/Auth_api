from src.infrastructure.database.db.connection import db
from .base import BaseRepository
from datetime import date, datetime

from sqlalchemy import select, update

from ..models.user import TableUserModel

from src.domain import Profile, UpdateProfile


class UserProfile(BaseRepository):
    def __init__(self):
        super().__init__(db.async_session_maker)

    async def user_profile(self, user_id: int) -> Profile|None:
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

    async def update_user_profile(self, profile_data: UpdateProfile, user_id: int) -> bool:
        try:
            update_data = {k: v for k, v in dict(profile_data).items() if v is not None}
            if profile_data.birthday is not None:
                update_data["age"] = int(date.today().year - profile_data.birthday.year - (
                            (date.today().month, date.today().day) < (profile_data.birthday.month, profile_data.birthday.day)))
            async with self.session() as session:
                user_params = update(TableUserModel).where(TableUserModel.id == user_id).values(**update_data)
                await session.execute(user_params)
                await session.commit()
                return True
        except Exception as e:
            return False

    async def delete_user_profile(self, user_id: int) -> bool:
        try:
            async with self.session() as session:
                delete = update(TableUserModel).where(TableUserModel.id == user_id).values(delete_profile=True, delete_profile_at= datetime.now())
                await session.execute(delete)
                await session.commit()
                return True
        except Exception as e:
            return False

