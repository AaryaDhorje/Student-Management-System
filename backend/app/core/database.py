# Database connection and session management

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    # Import all models to ensure they are registered with Base
    from ..models.student import Student
    from ..models.course import Course
    from ..models.enrollment import Enrollment
    from ..models.user import User
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
