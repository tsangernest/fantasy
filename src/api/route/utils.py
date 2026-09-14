from fastapi import APIRouter
from sqlalchemy import select
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from src.api.deps import SessionDep


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get(path="/health-web", response_model=None)
async def health_web_check():
    return {HTTP_200_OK: "FastAPI is okay!"}


@router.get(path="/health-db", response_model=None)
async def health_db_check(session: SessionDep) -> dict:
    results = await session.execute(select(1))
    result = results.scalar_one_or_none()
    if 1 == result:
        return {HTTP_200_OK: "Database is alive!"}
    return {HTTP_500_INTERNAL_SERVER_ERROR: "No database detected?"}

