"""Database engine configuration with async SQLModel."""

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.core.config import settings


# Create async engine with connection pooling
engine: AsyncEngine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=10,  # Number of connections to keep in pool
    max_overflow=20,  # Extra connections when pool is full
    pool_pre_ping=True,  # Verify connections before using
)
