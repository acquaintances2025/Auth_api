from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.infrastructure import BaseResponseController

test_router = APIRouter(tags=["healthz"])

@test_router.get("/healthz")
async def healthz():
    return JSONResponse(status_code=200, content=BaseResponseController.create_success_response("Запущен"))
