
from typing import Any
from contextlib import asynccontextmanager
import aiosqlite

import app.config


class AsyncSQLiteDB:

    def __init__(self, db_path: str):
        self.db_path = db_path

    @asynccontextmanager
    async def get_connection(self) -> aiosqlite.Connection:
        "async connection manager"
        conn = await aiosqlite.connect(self.db_path)
        try:
            yield conn
        finally:
            await conn.close()    
    
    # no ORM machinery needed for such a simple task, just plain SQL

    async def create_tables(self):

        async with self.get_connection() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS sequences (
                    name TEXT PRIMARY KEY,
                    ival INTEGER not null default 0
                )
            ''')
            await conn.execute('''
               insert or ignore into sequences (name, ival) values ('code', 0)
            ''')
            await conn.commit()

        async with self.get_connection() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS short_urls (
                    code        TEXT PRIMARY KEY,
                    orig_url    TEXT not null,
                    created_at  TIMESTAMP default CURRENT_TIMESTAMP,
                    redir_count INTEGER not null default 0
                )
            ''')
            await conn.commit()


    async def next_ival(self, seq_name: str = 'code') -> int:
        async with self.get_connection() as conn:
            async with conn.execute(
                'update sequences set ival=ival+1 where name=? returning ival', (seq_name,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    raise ValueError(f'Sequence not found: {seq_name}')
                await conn.commit()
                return row[0]


    async def insert_url(self, code: str, url: str):
        async with self.get_connection() as conn:
            await conn.execute(
                'insert into short_urls (code, orig_url) values (?, ?)', (code, url)
            )
            await conn.commit()


    async def get_stats(self, code: str) -> dict[str, Any] | None:
        async with self.get_connection() as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(
                'select orig_url, created_at, redir_count from short_urls where code=?', (code,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                return dict(row)


    async def do_redir(self, code: str) -> str | None:
        async with self.get_connection() as conn:
            async with conn.execute(
                'update short_urls set redir_count=redir_count+1 where code=? returning orig_url', (code,)
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                await conn.commit()
                return row[0]


def get_db():
    return AsyncSQLiteDB(app.config.DB_FILE)
