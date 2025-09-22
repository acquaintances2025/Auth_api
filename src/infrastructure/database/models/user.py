from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from src.domain import UserModel

from .base import BaseModel


class TableUserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, nullable=True)
    number = Column(String, nullable=True)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    birthday = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=True, default=False)
    created_at = Column(DateTime, nullable=False)
    block_at = Column(DateTime, nullable=True)
    active_phone = Column(Boolean, nullable=True, default=False)
    active_email = Column(Boolean, nullable=True, default=False)
    # data_object_id = Column(Integer, ForeignKey("app_datacall.id"))

    # data_object = relationship("DataCallModel", back_populates="meta_info")

    async def to_entity(self) -> UserModel:
        return await super().to_entity(UserModel)

    @classmethod
    async def from_entity(cls, entity: UserModel) -> 'UserModel':
        return await super().from_entity(entity)
