import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from app.core.logging import logger

DATABASE_URL = settings.SUPABASE_DB_URL

# For SQLite async compatibility: ensure URL is sqlite+aiosqlite:///
if DATABASE_URL.startswith("sqlite:///"):
    DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
elif DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

is_sqlite = DATABASE_URL.startswith("sqlite")

engine_kwargs = {
    "echo": False,
    "future": True,
}

if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Postgres pooling parameters
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20
    engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(DATABASE_URL, **engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_db():
    """Initializes tables for local sqlite or when starting fresh."""
    try:
        async with engine.begin() as conn:
            # Import models to ensure they are registered with Base.metadata
            from app.models import (
                Profile, CareerPreference, CandidateProfile, Resume,
                ResumeAnalysis, JobSource, Job, JobMatch, SavedJob,
                Application, Notification, JobIngestionRun, UserActivity
            )
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schema initialized successfully.")

        # Seed initial demo opportunities if database is fresh
        try:
            from sqlalchemy import select
            async with AsyncSessionLocal() as session:
                from app.models.all_models import Job
                res = await session.execute(select(Job.id).limit(1))
                if not res.scalar_one_or_none():
                    from app.seed_demo import seed_database
                    await seed_database()
        except Exception as seed_err:
            logger.warning(f"Auto-seed during init_db skipped/failed: {seed_err}")
    except Exception as e:
        logger.error(f"Error during init_db: {e}")
        # In production Supabase, migrations manage the schema

