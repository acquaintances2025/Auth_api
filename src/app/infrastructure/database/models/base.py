from typing import TypeVar, Type, Any
from sqlalchemy.orm import DeclarativeBase

T = TypeVar('T')

class BaseModel(DeclarativeBase):
    __abstract__ = True

    EXCLUDE_FROM_ENTITY_FIELDS = []

    async def to_entity(self, entity_class: Type[T]) -> T:
        """Преобразует модель в сущность"""
        return entity_class.model_validate(self)
    
    @classmethod
    async def from_entity(cls, entity: Any) -> 'BaseModel':
        """Создает модель из сущности"""
        exclude_fields = cls.EXCLUDE_FROM_ENTITY_FIELDS
        return cls(**entity.model_dump(exclude_unset=True, exclude=exclude_fields))