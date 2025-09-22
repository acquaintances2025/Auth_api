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
                                content={"answer": "Отсутствует обязательный параметр (номер телефона/email) при регистрации."})
        if user_data.password != user_data.confirm_password:
            return JSONResponse(
                status_code=400,
                content={"answer": "Введенные пароли не совпадают"}
            )
        else:
            if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$', user_data.password) is None:
                return JSONResponse(
                    status_code=400,
                    content={"answer": "Нарушение правил общепринятого стандарта паролей."}
                )
            hash_password = await get_password_hash(user_data.password)

        if user_data.email is not None:
            try:
                email_check = validate_email(user_data.email, check_deliverability=False)
                email = email_check.normalized
            except EmailNotValidError:
                return JSONResponse(
                    status_code=400,
                    content={"answer": "Email не соответствует стандарту"}
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
                content={"answer": "Данный пользователь уже зарегистрирован"}
            )

        uuid_user= uuid.uuid4()
        add_user = await UserWorks().create_user(uuid_user, email, phone, hash_password, user_data.name, user_data.lastname, user_data.surname, user_data.birthday)
        if add_user is not None:
            access_token = await create_access_token(uuid_user)
            refresh_token = await create_refresh_token(uuid_user)
            await TokenWorks().create_token(add_user, access_token, refresh_token)
        confirmation_code = random.randint(10000, 99999)
        await CodeWorks().create_confirmation_code(add_user, confirmation_code)
        if email is not None:
            sent_answer = await send_email(email, confirmation_code)

            if sent_answer is True:
                return JSONResponse(
                    status_code=200,
                    content={"access_token": access_token, "refresh_token": refresh_token}
                )
            else:
                return JSONResponse(
                    status_code=400,
                    content="В процессе отправки письма произошла ошибка"
                )
        #метод регистрации пользователя по номеру телефона, разблокировать в лучшие времена (рабочее)
        # if phone is not None:
        #     await send_number(phone, confirmation_code)


    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


async def confirm_registration(code, token):
    try:
        payload, error = await decode_token(token)
        if error is False:
            return JSONResponse(
                status_code=401,
                content={"answer": "Срок жизни токена истек"}
            )
        check_user_code = await UserWorks().confirmation_registration(payload["uuid_user"], code)
        if check_user_code is True:
            return JSONResponse(status_code=200, content={"answer": "Учетная запись пользователя активирована."})
        else:
            return JSONResponse(status_code=400, content={"answer":"Не удалась активировать учетную запись, возможно срок жизни кода подтверждения истек повторите попытку"})
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})