
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain import UpdateProfile, ConfirmationEmail
from .path import GET_PROFILE, UPDATE_PROFILE, DELETE_PROFILE, CONFIRMATION_EMAIL, CONFIRMATION_PHONE
from .views import get_user_profile, update_profile, delete_user_profile, sent_code_on_email

profile_router = APIRouter(prefix="/profiles", tags=["profile"])

security = HTTPBearer(auto_error=False)

@profile_router.get(GET_PROFILE)
async def get_profile(user_id: int = Query(description="Id Пользователя")):
    result = await get_user_profile(user_id)
    return result

@profile_router.put(UPDATE_PROFILE)
async def put_update_profile(profile_data: UpdateProfile):
    result = await update_profile(profile_data)
    return result

@profile_router.delete(DELETE_PROFILE)
async def delete_profile(user_id: int = Query(description="Id Пользователя")):
    result = await delete_user_profile(user_id)
    return result

@profile_router.put(CONFIRMATION_EMAIL)
async def confirmation_email(user_data: ConfirmationEmail):
    result = await sent_code_on_email(user_data.user_id, user_data.email)
    return result

@profile_router.put(CONFIRMATION_PHONE)
async def put_update_profile(phone: str = Query(description="Номер телефона пользователя")):
    result = await confirmation_user_phone(phone)
    return result