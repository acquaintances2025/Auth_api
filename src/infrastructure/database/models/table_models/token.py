from sqlalchemy import Column, Integer, String, ForeignKey


from ..base import BaseModel
from ..query_models.token_entity import TokenModel

class UserTokenModel(BaseModel):
    __tablename__ = 'user_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)

    async def to_entity(self) -> TokenModel:
        return await super().to_entity(TokenModel)

    @classmethod
    async def from_entity(cls, entity: TokenModel) -> 'TokenModel':
        return await super().from_entity(entity)
