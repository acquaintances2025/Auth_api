import random
import re

from select import error
from datetime import datetime, timedelta

from src.infrastructure import BaseResponseController, send_email, UserProfile, CodeWorks, send_phone, UserWorks

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
        await CodeWorks().create_confirmation_code(user_id, confirmation_code, "confirmation_email")
        return JSONResponse(status_code=200,
                            content=BaseResponseController().create_success_response(
                                "Отправлен код подтверждения на указанный email.").dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось отправить код подтверждения на указанный email, повторите попытку.").dict())


async def sent_code_on_phone(user_id: int, phone: str) -> JSONResponse:
    if user_id is not None:
        phone = re.sub(r'\D', '', phone)
        if phone.startswith('8'):
            phone = '7' + phone[1:]
        elif phone.startswith('7'):
            pass
        else:
            phone = '7' + phone
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не верно указан номер телефона.").dict())
    confirmation_code = random.randint(10000, 99999)

    # sent_answer = await send_phone(phone, confirmation_code)
    sent_answer = True
    if sent_answer is True:
        await CodeWorks().create_confirmation_code(user_id, confirmation_code, "confirmation_phone")
        return JSONResponse(status_code=200,
                            content=BaseResponseController().create_success_response(
                                "Отправлен код подтверждения на указанный номер телефона.").dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось отправить код подтверждения на указанный номер телефона, повторите попытку.").dict())

async def completion_number_or_phone(user_id: int, code: int, email: str|None, phone: str|None) -> JSONResponse:
    if email is None and phone is None:
        return JSONResponse(status_code=400,
                            content=BaseResponseController().create_error_response(
                                "Не удалось определить параметр подтверждения (number/phone).").dict())

    completion = await CodeWorks().check_confirmation_code(user_id, code)
    if completion:
        if completion["type"] in ["confirmation_email", "confirmation_phone"] and (datetime.now() - completion["created_at"] < timedelta(minutes=10)) is True:
            if completion["type"].split("_")[1] == "email" and email is not None:
                error, answer = await UserWorks().completion_confirmation_email(user_id, email)
                if error is False:
                    return JSONResponse(status_code=400, content=BaseResponseController().create_success_response(answer).dict())
                else:
                    await CodeWorks().blok_confirmation_code(user_id, code)
                    return JSONResponse(status_code=200, content=BaseResponseController().create_success_response(answer).dict())
            elif completion["type"].split("_")[1] == "phone" and phone is not None:
                error, answer = await UserWorks().completion_confirmation_phone(user_id, phone)
                if error is False:
                    return JSONResponse(status_code=400, content=BaseResponseController().create_success_response(answer).dict())
                else:
                    await CodeWorks().blok_confirmation_code(user_id, code)
                    return JSONResponse(status_code=200, content=BaseResponseController().create_success_response(answer).dict())
        else:
            return JSONResponse(status_code=400,
                                content=BaseResponseController().create_error_response(
                                    "Срок жизни кода истек, повторите попытку.").dict())
    else:
        return JSONResponse(status_code=400,
                            content=BaseResponseController().create_error_response(
                                "Не удалось найти код подтверждения.").dict())
