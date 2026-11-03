from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

from app.core.config import settings

# Database engine
engine=create_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True
)

# Database session factory
SessionLocal=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False  
)
# Base class for database models
class Base(DeclarativeBase):
    pass