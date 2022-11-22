# test_main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import PlainTextResponse
from app.core.config import settings
from app.core.router import users, robots, game
from app.core.models.base import define_database_and_entities

define_database_and_entities(
    provider=settings.DB_PROVIDER, filename=settings.DB_TEST_NAME, create_db=True)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(users.router)
    _app.include_router(robots.router)
    _app.include_router(game.router)

    return _app


app_test = get_application()


@app_test.exception_handler(RequestValidationError)
@app_test.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)
