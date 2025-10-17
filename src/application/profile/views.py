import random

from src.infrastructure import BaseResponseController, send_email, UserProfile, CodeWorks

from starlette.responses import JSONResponse
from email_validator import validate_email, EmailNotValidError



async def get_user_profile(user_id: int) -> JSONResponse:
    user_profiles = await UserProfile().user_profile(user_id)
    user_profiles.created_at = user_profiles.created_at.strftime('%d.%m.%Y %H:%M:%S')
    user_profiles.birthday = user_profiles.birthday.strftime('%d.%m.%Y %H:%M:%S')
    return JSONResponse(status_code=200, content=BaseResponseController().create_success_response("Успешное выполнение запроса.", user_profiles).dict())

async def update_profile(profile_data) -> JSONResponse:
    update_user = await UserProfile().update_user_profile(profile_data)
    if update_user:
        return JSONResponse(status_code=200,
                            content=BaseResponseController().create_success_response("Успешное выполнение запроса.").dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось обновить параметры пользователя, повторите позже.").dict())

async def delete_user_profile(user_id: int) -> JSONResponse:
    delete_user = await UserProfile().delete_user_profile(user_id)
    if delete_user:
        return JSONResponse(status_code=200,
                            content=BaseResponseController().create_success_response("Профиль пользователя переведен в статус 'Удален', Вы можете восстановить его в течении 30 дней.").dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось удалить профиль пользователя, повторите попытку.").dict())


async def sent_code_on_email(user_id: int, email: str) -> JSONResponse:
    try:
        email_check = validate_email(email, check_deliverability=False)
        email = email_check.normalized
    except EmailNotValidError:
        return JSONResponse(
            status_code=400,
            content=BaseResponseController().create_error_response("Email не соответствует стандарту.").dict()
        )
    confirmation_code = random.randint(10000, 99999)

    sent_answer = await send_email(email, confirmation_code)
    if sent_answer is True:
        await CodeWorks().create_confirmation_code(user_id, confirmation_code, "confirmation")
        return JSONResponse(status_code=200,
                            content=BaseResponseController().create_success_response(
                                "Отправлен код подтверждения на указанный email.").dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось отправить код подтверждения на указанный email, повторите попытку.").dict())





async def confirmation_user_phone(phone: str) -> JSONResponse:
    confirmation = await UserProfile().sending_code_on_phone(phone)
    if confirmation:
        return JSONResponse(status_code=200,
                            content=BaseResponseController().create_success_response("Отправлен код подтверждения на указанный номер телефона.").dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось отправить код подтверждения на указанный номер телефона, повторите попытку.").dict())
