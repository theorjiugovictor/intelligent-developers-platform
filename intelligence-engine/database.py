"""
Database models and connection management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import settings
import logging

logger = logging.getLogger(__name__)

# Import monitoring for DB operations tracking
try:
    from monitoring import db_operations_total
except ImportError:
    db_operations_total = None

# Convert postgresql:// to postgresql+asyncpg://
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://"
)

# Async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Async session
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync engine for migrations
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()

async def init_db():
    """Initialize database"""
    try:
        async with async_engine.begin() as conn:
            # Create tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        if getattr(settings, 'ALLOW_DB_INIT_FAILURE', False):
            logger.warning(f"Database initialization failed but continuing (ALLOW_DB_INIT_FAILURE=True): {e}")
        else:
            logger.error(f"Error initializing database: {e}")
            raise

async def get_db():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
            # Track successful DB operations
            if db_operations_total:
                db_operations_total.labels(operation="commit", status="success").inc()
        except Exception:
            await session.rollback()
            # Track failed DB operations
            if db_operations_total:
                db_operations_total.labels(operation="rollback", status="error").inc()
            raise
        finally:
            await session.close()
