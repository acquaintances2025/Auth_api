from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.infrastructure import logger
from src.config.settings import Config

from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.user: str = Config.PSQL_DB_USER
        self.password: str = Config.PSQL_DB_PASSWORD
        self.db_name: str = Config.PSQL_DB_NAME
        self.host: str = Config.PSQL_DB_HOST
        self.port: str = Config.PSQL_DB_PORT

        self.DATABASE_URL = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_async_engine(self.DATABASE_URL, echo=False)
        self.async_session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

    async def create_session_pool(self):
        logger.info("Создан пул к базе данных")
        return


db = Database()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.async_session_maker() as session:
        yield session