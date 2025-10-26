from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from database.models.User import User


DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"

# Async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Async context manager
@asynccontextmanager
async def get_async_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Example usage
import asyncio
from sqlalchemy.future import select

async def fetch_users():
    async with get_async_db_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print([user.name for user in users])

if __name__ == "__main__":
    asyncio.run(fetch_users())
