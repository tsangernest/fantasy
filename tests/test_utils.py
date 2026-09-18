import pytest

from httpx import AsyncClient as httpxAsyncClient
from sqlalchemy import select
from starlette import status

from src.api.deps import SessionDep


@pytest.mark.anyio
async def test_health_web(aclient: httpxAsyncClient):
    response = await aclient.get(url="/utils/health-web")
    assert status.HTTP_200_OK == response.status_code
    json_response = response.json()
    assert json_response == {"200": "FastAPI is okay!"}


@pytest.mark.anyio
async def test_health_db(aclient: httpxAsyncClient, session: SessionDep):
    results = await session.execute(select(1))
    result = results.scalar_one_or_none()
    assert 1 == result

