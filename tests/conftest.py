from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient as httpxAsyncClient
from sqlalchemy import select

from src.api.deps import SessionDep, get_db
from src.core.db import init_db
from src.main import get_application


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[SessionDep, None]:
    """
    async for session in get_db(): # because we have multiple session of multiple users
    """
    async for session in get_db():
        await session.execute(select(1))
        await session.commit()
        yield session


@pytest.fixture(scope="module")
async def app() -> AsyncGenerator[FastAPI, None]:
    app = get_application()
    await init_db()
    # print(f"{app.host=}")
    yield app


@pytest.fixture(scope="module")
async def aclient(app) ->  AsyncGenerator[httpxAsyncClient, None]:
    async with httpxAsyncClient(base_url="http://localhost:8000") as aclient:
        yield aclient

