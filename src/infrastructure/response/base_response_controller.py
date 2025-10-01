from typing import Optional, TypeVar, Generic, Any
from src.domain import BaseResponse
from ..loggings.logger import logger

T = TypeVar('T')


class BaseResponseController(Generic[T]):

    def create_response(self, is_success: bool, message: str, data: Optional[T] = None) -> BaseResponse[T]:
        return BaseResponse(isSuccess=is_success, message=message, data=data)

    def create_success_response(self, message: str, data: Optional[T] = None) -> BaseResponse[T]:
        return self.create_response(True, message, data)

    def create_error_response(self, message: str, data: Optional[T] = None) -> BaseResponse[T]:
        logger.error(f"Ошибка: {message}")
        return self.create_response(False, message, data)