from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError

from typing import Any

from src.application import test_router, auth_router, profile_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Gateway API",
        version="0.0.1",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["DNT", "X-CustomHeader", "Keep-Alive", "User-Agent", "X-Requested-With",
                       "If-Modified-Since", "Cache-Control", "Content-Type", "x-tz-offset", "Authorization"],
    )

    async def default_exception_handler(request: Request, exc: Any) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"message": "Ошибка исполнения процесса."}
        )

    app.default_exception_handler = default_exception_handler

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        if exc.detail == "Not authenticated":
            return JSONResponse(
                status_code=400, content={"message": "Параметры входа не соответствуют верным."}
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc) -> JSONResponse:
        if hasattr(exc, "body") and exc.body is None:
            return JSONResponse(
                status_code=400,
                content={"message": "Отсутствуют параметры запроса"}
            )
        return JSONResponse(
            status_code=400,
            content={"message": "Параметры входа не соответствуют верным."}
        )

    app.include_router(test_router)
    app.include_router(auth_router)
    app.include_router(profile_router)

    return app