import uuid
import re
import random

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.infrastructure import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
    get_password_hash,
    send_email,
    send_number,
    BaseResponseController,
    logger)

from src.infrastructure.database import (
    UserWorks,
    TokenWorks,
    CodeWorks)

from email_validator import validate_email, EmailNotValidError

async def create_user(user_data):
    try:
        if user_data.email is None and user_data.number is None:
            return JSONResponse(status_code=400,
                                content=BaseResponseController().create_error_response("Отсутствует обязательный параметр (номер телефона/email) при регистрации.").dict()
                                )
        if user_data.password != user_data.confirm_password:
            return JSONResponse(
                status_code=400,
                content=BaseResponseController().create_error_response("Введенные пароли не совпадают.").dict()
            )
        else:
            if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$', user_data.password) is None:
                return JSONResponse(
                    status_code=400,
                    content=BaseResponseController().create_error_response("Нарушение правил общепринятого стандарта паролей.").dict()
                )
            hash_password = await get_password_hash(user_data.password)

        if user_data.email is not None:
            try:
                email_check = validate_email(user_data.email, check_deliverability=False)
                email = email_check.normalized
            except EmailNotValidError:
                return JSONResponse(
                    status_code=400,
                    content=BaseResponseController().create_error_response("Email не соответствует стандарту.").dict()
                )
        else:
            email = None

        if user_data.number is not None:
            phone = re.sub(r'\D', '', user_data.number)
            if phone.startswith('8'):
                phone = '7' + phone[1:]
            elif phone.startswith('7'):
                pass
            else:
                phone = '7' + phone
        else:
            phone = None


        check_user = await UserWorks().check_user(email, phone, user_data.name, user_data.lastname, user_data.surname, user_data.birthday)
        if check_user is not None:
            return JSONResponse(
                status_code=400,
                content=BaseResponseController().create_error_response("Данный пользователь уже зарегистрирован.").dict()
            )

        uuid_user= uuid.uuid4()
        add_user = await UserWorks().create_user(uuid_user, email, phone, hash_password, user_data.name, user_data.lastname, user_data.surname, user_data.birthday)
        if add_user is not None:
            access_token = await create_access_token(add_user["id"], add_user["role"])
            refresh_token = await create_refresh_token(add_user["id"], add_user["role"])
            await TokenWorks().create_token(add_user["id"], access_token, refresh_token)
        confirmation_code = random.randint(10000, 99999)
        await CodeWorks().create_confirmation_code(add_user["id"], confirmation_code, "registration")
        if email is not None:
            sent_answer = await send_email(email, confirmation_code)

            if sent_answer is True:
                return JSONResponse(
                    status_code=200,
                    content=BaseResponseController().create_success_response("Успешное выполнение запроса.", {"access_token": access_token, "refresh_token": refresh_token}).dict()
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content=BaseResponseController().create_error_response("В процессе отправки письма произошла ошибка.").dict()
                )
        #метод регистрации пользователя по номеру телефона, разблокировать в лучшие времена (рабочее)
        # if phone is not None:
        #     await send_number(phone, confirmation_code)


    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response("Возникла ошибка исполнения процесса.").dict())


async def confirm_registration(code, token):
    try:
        payload, error = await decode_token(token)
        if error is False:
            return JSONResponse(
                status_code=401,
                content=BaseResponseController().create_error_response("Срок жизни токена истек.").dict()
            )
        check_user_code = await UserWorks().confirmation_registration(payload["user_id"], code)
        if check_user_code is True:
            return JSONResponse(status_code=200, content=BaseResponseController().create_success_response("Учетная запись пользователя активирована.").dict())
        else:
            return JSONResponse(status_code=400, content=BaseResponseController().create_error_response("Не удалась активировать учетную запись, возможно срок жизни кода подтверждения истек повторите попытку.").dict())
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content=BaseResponseController().create_error_response("Возникла ошибка исполнения процесса.").dict())

async def auth_user(auth_data):
    user, error = await UserWorks().authorization_user(auth_data.email, auth_data.phone, auth_data.password)
    if user is not None:
        access_token = await create_access_token(user["id"], user["role"])
        refresh_token = await create_refresh_token(user["id"], user["role"])
        user_token_update = await UserWorks().update_user_token(int(user["id"]), access_token, refresh_token)
        if user_token_update is True:
            return JSONResponse(
                status_code=200,
                content=BaseResponseController().create_success_response("Успешное выполнение запроса", {"access_token": access_token, "refresh_token": refresh_token}).dict()
            )
        else:
            return JSONResponse(status_code=400, content=BaseResponseController().create_error_response("Не удалось обновить токен доступа пользователя, повторите попытку").dict())
    else:
        return JSONResponse(status_code=401, content=BaseResponseController().create_error_response("Логин или пароль не верен. Либо аккаунт деактивирован, попробуйте восстановить его.").dict())

async def password_recovery(email, token=None, phone=None):
    if token is not None:
        payload, error = await decode_token(token.credentials)
        if error is False:
            return JSONResponse(
                status_code=401,
                content=BaseResponseController().create_error_response("Срок жизни токена истек.").dict()
            )
        user_id = int(payload["user_id"])
        email = await UserWorks().check_user_in_user_id(user_id)
    else:
        user_id = await UserWorks().check_user_in_email_or_phone(email, phone)
        if user_id is None:
            return JSONResponse(
                status_code=400,
                content=BaseResponseController().create_error_response("Пользователь не найден.").dict()
            )
    confirmation_code = random.randint(10000, 99999)
    await CodeWorks().create_confirmation_code(user_id, confirmation_code, "password_recovery")
    if email is not None:
        sent_answer = await send_email(email, confirmation_code)
        if sent_answer is True:
            return JSONResponse(status_code=200, content=BaseResponseController().create_success_response("Код подтверждения отправлен на указанный email.", {"user_id": user_id}).dict())
        else:
            return JSONResponse(status_code=400, content=BaseResponseController().create_error_response("Не удалось отправить код подтверждения на указанный email.").dict())

    # метод регистрации пользователя по номеру телефона, разблокировать в лучшие времена (рабочее)
    # if phone is not None:
    #     await send_number(phone, confirmation_code)


async def user_password_update(user_data):

    if user_data.password != user_data.confirm_password:
        return JSONResponse(
            status_code=400,
            content=BaseResponseController().create_error_response("Введенные пароли не совпадают").dict()
        )
    else:
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$', user_data.password) is None:
            return JSONResponse(
                status_code=400,
                content=BaseResponseController().create_error_response(
                    "Нарушение правил общепринятого стандарта паролей.").dict()
            )
    check_user_code, answer = await UserWorks().check_user_code_in_user_id(user_data.user_id, user_data.code)
    if check_user_code is True:
        hash_password = await get_password_hash(user_data.password)
        new_password, answer = await UserWorks().update_password(hash_password, user_data.user_id)
        if new_password is True:
            return JSONResponse(
                status_code=200,
                content=BaseResponseController().create_success_response(
                    answer).dict()
            )
        else:
            return JSONResponse(
                status_code=400,
                content=BaseResponseController().create_error_response(
                    answer).dict()
            )

    else:
        return JSONResponse(
            status_code=400,
            content=BaseResponseController().create_error_response(
                answer).dict()
        )


async def user_refresh_update(request):
    payload, error = await decode_token(request.cookies["Hive"])
    if error is False:
        user_id = await UserWorks().user_id_in_refresh(request.cookies["Hive"])
        access_token = await create_access_token(user_id, payload["role"])
        refresh_token = await create_refresh_token(user_id, payload["role"])
    else:
        access_token = await create_access_token(payload["user_id"], payload["role"])
        refresh_token = await create_refresh_token(payload["user_id"], payload["role"])
    user_token_update = await UserWorks().update_user_token(payload["user_id"], access_token, refresh_token)
    if user_token_update is True:
        return JSONResponse(
            status_code=200,
            content=BaseResponseController().create_success_response("Успешное выполнение запроса.",
                                                                     {"access_token": access_token, "refresh_token": refresh_token}).dict())
    else:
        return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
            "Не удалось обновить токен доступа пользователя, повторите попытку.").dict())

