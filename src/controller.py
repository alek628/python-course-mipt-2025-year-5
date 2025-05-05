import asyncpg
from asyncpg import Pool

from config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)


class DBConnection:
    """Class that provides single connection pool
    per FatAPI instance
    """

    pool: Pool = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance  # type: ignore

    def __init__(
        self,
        disable_ssl: bool = False,
        min_size: int = 1,
        max_size: int = 4,
    ):
        if disable_ssl:
            self.ssl = None
        else:
            self.ssl = "require"

        self.min_size = min_size
        self.max_size = max_size

    async def connect(self) -> Pool:
        """Creates single connection for database per app

        :return:
        """
        if self.pool:
            return self.pool
        self.pool = await asyncpg.create_pool(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            max_size=self.max_size,
            min_size=self.min_size,
        )

    async def close(self):
        if self.pool:
            await self.pool.close()
