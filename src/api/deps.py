from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core.db import engine


async def get_db():
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]

