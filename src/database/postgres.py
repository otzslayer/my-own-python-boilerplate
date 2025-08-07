from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

ASYNC_DATABASE_URL = "your_async_database_url"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
