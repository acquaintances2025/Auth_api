import src.application.auth.path as p

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain import RegistrationUser, ConfirmationUser, AuthUser, PasswordUpdate
from src.infrastructure import logger, BaseResponseController
from .views import create_user, confirm_registration, auth_user, password_recovery, user_password_update, user_refresh_update

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer(auto_error=False)


@auth_router.post(p.REGISTRATION)
async def registration_user(user_data: RegistrationUser):
    try:
       result = await create_user(user_data)
       return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response("Возникла ошибка исполнения процесса.").dict())

@auth_router.post(p.CONFIRMATION)
async  def confirmation_user(code: ConfirmationUser,
                             token: HTTPAuthorizationCredentials | None = Depends(security)):
    try:
        result = await confirm_registration(code.code, token.credentials)
        return result
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response("Возникла ошибка исполнения процесса.").dict())


@auth_router.post(p.AUTHORIZATION)
async def authorization_user(user_data: AuthUser):
    try:
        result = await auth_user(user_data)
        return result
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response("Возникла ошибка исполнения процесса.").dict())


@auth_router.get(p.PASSWORDRECOVERY)
async def user_password_recovery(email: str = Query(default=None, description="Email пользователя для восстановления пароля"),
                                 token: HTTPAuthorizationCredentials | None = Depends(security)
                                 # phone: str = Query(default=None, description="Номер телефона пользователя")
                                 ):
    try:
        result = await password_recovery(email, token)
        return result
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response("Возникла ошибка исполнения процесса.").dict())


@auth_router.post(p.PASSWORDUPDATE)
async def password_update(user_data: PasswordUpdate):
    try:
        result = await user_password_update(user_data)
        return result
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса.").dict())


@auth_router.get(p.REFRESHUPDATE)
async def refresh_update(request: Request):
    try:
        result = await user_refresh_update(request)
        return result
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response(
            "Возникла ошибка исполнения процесса.").dict())