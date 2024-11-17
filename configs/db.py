import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from configs.env import settings

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


if ENVIRONMENT == "development":
    DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
else:
    DATABASE_URL = "postgresql://admin:admin123@localhost:5432/profile_test"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    """
    Function to get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


