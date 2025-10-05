from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from .path import GET_PROFILE
from .views import get_user_profile

profile_router = APIRouter(prefix="/profiles", tags=["profile"])

security = HTTPBearer(auto_error=False)

@profile_router.get(GET_PROFILE)
async def get_profile(token: HTTPAuthorizationCredentials | None = Depends(security)):
    result = await get_user_profile(token)
    return result