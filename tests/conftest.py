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
    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
    PARAMS = {"lang": "en", "region": "us"}
    HEADERS = {"Accept": "application/json", "Accept-Language": "en-US,en;q=0.8", "Referrer": "https://www.google.com"}

    # Can include this once I figure out how to add this into the fixture
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    async with httpxAsyncClient(
            base_url=BASE_URL,
            params=PARAMS,
            headers=HEADERS,
    ) as aclient:
        yield aclient

