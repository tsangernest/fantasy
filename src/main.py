from fastapi import FastAPI

from src.api.main import api_router
from src.core.db import init_db


async def on_startup():
    await init_db()


def get_application() -> FastAPI:
    application = FastAPI(debug=True)
    application.include_router(api_router)
    return application


app = get_application()

