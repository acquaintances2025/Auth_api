from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .path import AUTHORIZATION, REGISTRATION, CONFIRMATION

from app.domain import RegistrationUser, ConfirmationUser, AuthUser
from app.infrastructure import logger
from .views import create_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])



@auth_router.post(REGISTRATION, summary="Регистрация пользователя",
                  response_description="Отправка письма/sms подтверждения",
                  responses={
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Код подтверждения успешно отправлен",
                        "data": {}
                    }
                }
            }
        },
        "400": {
            "description": "Ошибка в запросе"
        },
        "500": {
            "description": "Внутренняя ошибка сервера"
        }
    }
                  )
async def authorization_user(user_data: RegistrationUser):
    # try:
       result = await create_user(user_data)
       return result
    # except Exception as exc:
    #     logger.error(f"Ошибка исполнения процесса {exc}")
    #     return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


@auth_router.post(CONFIRMATION,
                  summary="Подтверждение регистрации пользователя",
                  response_description="Аккаунт пользователя подтвержден, создана учетная запись в базе данных",
                  responses={
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Успешное подтверждение учетной запись",
                        "data": {}
                    }
                }
            }
        },
        "400": {
            "description": "Ошибка в запросе"
        },
        "500": {
            "description": "Внутренняя ошибка сервера"
        }
    })
async  def confirmation_user(code: ConfirmationUser):
    try:
        pass
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


@auth_router.post(AUTHORIZATION,
                  summary="Вход пользователя в аккаунт",
                  response_description="Создается сессия пользователя, в cookies прописывается refresh token",
                  responses={
                      "200": {
                          "description": "Успешное выполнение запроса",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "isSuccess": True,
                                      "message": "Успешный вход в аккаунт",
                                      "data": {
                                          "acsses_token": "token"
                                      }
                                  }
                              }
                          }
                      },
                      "400": {
                          "description": "Ошибка в запросе"
                      },
                      "500": {
                          "description": "Внутренняя ошибка сервера"
                      }
                  })
async def authorization_user(user_data: AuthUser):
    try:
        pass
    except Exception as exc:
        logger.error(f"В процессе подтверждения пользователя произошла ошибка {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})
