import asyncio

import asyncpg

from data import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                dsn=config.POSTGRES_URI
                # user=config.PGUSER,
                # password=config.PGPASSWORD,
                # host=config.ip,
                # database=config.DATABASE
            )
        )

    async def create_table_users(self):
        sql="""
        CREATE TABLE IF NOT EXISTS Users (
        id INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Username VARCHAR(255),
        Lang VARCHAR(255),
        Translate VARCHAR(255),
        PRIMARY KEY (id)
        )        
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id: int, name: str, username: str = None, lang: str = None, translate: str = "en"):
        sql = "INSERT INTO Users (id, name, username, lang, translate) VALUES ($1, $2, $3, $4, $5)"
        try:
            await self.pool.execute(sql, id, name, username, lang, translate)
        except asyncpg.exceptions.UniqueViolationError:
            pass

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Users")

    async def get_translate(self, user_id):
        sql = "SELECT translate FROM Users WHERE id = $1"
        return await self.pool.fetchrow(sql, user_id)

    async def update_user_translate(self, translate, id):
        sql = "UPDATE Users SET translate = $1 WHERE id = $2"
        return await self.pool.execute(sql, translate, id)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE True")
