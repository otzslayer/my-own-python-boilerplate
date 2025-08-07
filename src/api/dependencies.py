from src.database.postgres import AsyncSessionLocal


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
