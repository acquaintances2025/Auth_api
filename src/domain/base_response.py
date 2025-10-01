from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    isSuccess: bool
    message: str
    data: Optional[T] = None
