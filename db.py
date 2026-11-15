from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# SQLite requires 'check_same_thread=False' when used with FastAPI's async threads; PostgreSQL does not
args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
# Create the core database engine using the configured URL
engine = create_engine(settings.database_url, connect_args=args)
# Create a factory for generating new database sessions per request
SessionLocal = sessionmaker(bind=engine)
# Base class that all database table models will inherit from
Base = declarative_base()
# Define the 'readings' table schema in the database
class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String, index=True)
    temperature = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
# Automatically create all defined tables in the database if they do not exist yet
Base.metadata.create_all(engine)