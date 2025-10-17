from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from src.domain import CodeModel

from .base import BaseModel

class ConfirmationCodeModel(BaseModel):
    __tablename__ = 'confirmation_code'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    type = Column(String, nullable=False)

    async def to_entity(self) -> CodeModel:
        return await super().to_entity(CodeModel)

    @classmethod
    async def from_entity(cls, entity: CodeModel) -> 'CodeModel':
        return await super().from_entity(entity)