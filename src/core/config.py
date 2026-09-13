from functools import lru_cache
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings


@lru_cache
class Settings(BaseSettings):
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username="fantasyuser",
            password="fantasypass",
            host="postgresql",
            port=5432,
            path="fantasy",
        )


settings = Settings()

