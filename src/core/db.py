from sqlalchemy import NullPool, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel

from src.core.config import settings


engine: AsyncEngine = create_async_engine(
    url=str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,
    future=True,
    poolclass=NullPool,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        try:
            await conn.execute(select(1))
            print(f"\nengine={engine.engine}\n")
        except IntegrityError:
            pass

