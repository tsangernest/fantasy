from fastapi import APIRouter
from sqlalchemy import select
from starlette.status import HTTP_200_OK


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get(path="/health-web", response_model=None)
async def health_web_check():
    return {HTTP_200_OK: "FastAPI is okay!"}


# @router.get(path="/health-db", response_model=None)

