import asyncio
import asyncpg
from . import connection

class Database:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host="localhost",
            port=5432,
            user="postgres",
            password="postgres",
            database="crop_yield",
            min_size=5,
            max_size=20,
        )
        print("Database connection pool created")
    
    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            print("Database connection pool closed")
    
    async def execute(self, query: str, *args, **kwargs):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args, **kwargs)
    
    async def fetch(self, query: str, *args, **kwargs):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args, **kwargs)
    
    async def fetchrow(self, query: str, *args, **kwargs):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args, **kwargs)
    
    async def fetchval(self, query: str, *args, **kwargs):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args, **kwargs)

# Global database instance
db = Database()

# Dependency to get DB pool
async def get_db():
    async with db.pool.acquire() as conn:
        yield conn