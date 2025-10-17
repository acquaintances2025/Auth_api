
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain import UpdateProfile
from .path import GET_PROFILE, UPDATE_PROFILE, DELETE_PROFILE
from .views import get_user_profile, update_profile, delete_user_profile

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