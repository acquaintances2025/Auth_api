import uuid
import re
import random

from fastapi.responses import JSONResponse

from app.infrastructure import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
    get_password_hash,
    send_email,
    send_number,
    logger)

from app.infrastructure.database import (
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
            number = re.sub(r'\D', '', user_data.number)
            if number.startswith('8'):
                number = '7' + number[1:]
            elif number.startswith('7'):
                pass
            else:
                number = '7' + number
        else:
            number = None


        check_user = await UserWorks().check_user(email, number)
        if check_user is not None:
            return JSONResponse(
                status_code=400,
                content={"answer": "Данный пользователь уже зарегистрирован"}
            )

        uuid_user= uuid.uuid4()
        add_user = await UserWorks().create_user(uuid_user, email, number, hash_password)
        if add_user is not None:
            access_token = await create_access_token(uuid_user)
            refresh_token = await create_refresh_token(uuid_user)
            await TokenWorks().create_token(add_user, access_token, refresh_token)
        confirmation_code = random.randint(10000, 99999)
        await CodeWorks().create_confirmation_code(add_user, confirmation_code)
        if email is not None:
            await send_email(email, confirmation_code)

        if number is not None:
            await send_number(number, confirmation_code)

        #todo дописать отправку токенов на gatewey api


    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})


async def confirm_registration(user_data):
    try:
        pass
    except Exception as exc:
        logger.error(f"Ошибка исполнения процесса {exc}")
        return JSONResponse(status_code=500, content={"answer": "Возникла ошибка исполнения процесса."})