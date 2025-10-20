from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse

from src.domain import UpdateProfile, ConfirmationEmail, ConfirmationPhone, CompletionCode
from src.infrastructure import logger, BaseResponseController

from .path import GET_PROFILE, UPDATE_PROFILE, DELETE_PROFILE, CONFIRMATION_EMAIL, CONFIRMATION_PHONE, COMPLETION_CONFIRMATION
from .views import get_user_profile, update_profile, delete_user_profile, sent_code_on_email, sent_code_on_phone, completion_number_or_phone


profile_router = APIRouter(prefix="/profiles", tags=["profile"])

security = HTTPBearer(auto_error=False)

@profile_router.get(GET_PROFILE)
async def get_profile(user_id: int = Query(description="Id Пользователя")):
    try:
        result = await get_user_profile(user_id)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса при получении профиля.").dict())


@profile_router.put(UPDATE_PROFILE)
async def put_update_profile(profile_data: UpdateProfile):
    try:
        result = await update_profile(profile_data)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса при обновлении профиля.").dict())

@profile_router.delete(DELETE_PROFILE)
async def delete_profile(user_id: int = Query(description="Id Пользователя")):
    try:
        result = await delete_user_profile(user_id)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса при удалении профиля.").dict())

@profile_router.put(CONFIRMATION_EMAIL)
async def confirmation_email(user_data: ConfirmationEmail):
    try:
        result = await sent_code_on_email(user_data.user_id, user_data.email)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса при отправке кода подтверждения на email.").dict())

@profile_router.put(CONFIRMATION_PHONE)
async def confirmation_phone(user_data: ConfirmationPhone):
    try:
        result = await sent_code_on_phone(user_data.user_id, user_data.phone)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса при отправке кода подтверждения на номер телефона.").dict())

@profile_router.put(COMPLETION_CONFIRMATION)
async def completion_confirmation(user_data: CompletionCode):
    try:
        result = await completion_number_or_phone(user_data.user_id, user_data.code, user_data.email, user_data.phone)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса при подтверждении номера телефона/email.").dict())