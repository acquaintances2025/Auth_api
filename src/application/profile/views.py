from src.infrastructure import decode_token, BaseResponseController

from src.infrastructure.database import UserProfile

from starlette.responses import JSONResponse


async def get_user_profile(token):
    user_id, error = await decode_token(token.credentials)
    if user_id is None:
        return JSONResponse(status_code=401, content=BaseResponseController().create_error_response("Токен пользователя просрочен.").dict())
    else:
        user_profiles = await UserProfile().user_profile(user_id["user_id"])
        user_profiles.created_at = user_profiles.created_at.strftime('%d.%m.%Y %H:%M:%S')
        user_profiles.birthday = user_profiles.birthday.strftime('%d.%m.%Y %H:%M:%S')
        return JSONResponse(status_code=200, content=BaseResponseController().create_success_response("Успешное выполнение запроса", user_profiles).dict())

async def update_profile(token, profile_data):
    user_id, error = await decode_token(token.credentials)
    if user_id is None:
        return JSONResponse(status_code=401, content=BaseResponseController().create_error_response("Токен пользователя просрочен.").dict())
    else:
        update_user = await UserProfile().update_user_profile(profile_data, user_id["user_id"])
        if update_user:
            return JSONResponse(status_code=200,
                                content=BaseResponseController().create_success_response("Успешное выполнение запроса").dict())
        else:
            return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
                "Не удалось обновить параметры пользователя, повторите позже.").dict())

async def delete_user_profile(token):
    user_id, error = await decode_token(token.credentials)
    if user_id is None:
        return JSONResponse(status_code=401, content=BaseResponseController().create_error_response("Токен пользователя просрочен.").dict())
    else:
        delete_user = await UserProfile().delete_user_profile(user_id["user_id"])
        if delete_user:
            return JSONResponse(status_code=200,
                                content=BaseResponseController().create_success_response("Профиль пользователя переведен в статус 'Удален', Вы можете восстановить его в течении 30 дней.").dict())
        else:
            return JSONResponse(status_code=400, content=BaseResponseController().create_error_response(
                "Не удалось профиль пользователя, повторите попытку.").dict())

