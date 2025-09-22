from fastapi import APIRouter

test_router = APIRouter(tags=["healthz"])

@test_router.get("/healthz")
async def healthz():
    return {"status": "ok"}