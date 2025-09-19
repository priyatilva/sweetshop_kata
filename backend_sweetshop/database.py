from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Check if running in test mode
TESTING = os.getenv("TESTING") == "1"

if TESTING:
    DATABASE_URL = "sqlite:///:memory:"  # in-memory DB for tests
else:
    DATABASE_URL = "sqlite:///./sweetshop.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
