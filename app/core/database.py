import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("variável de ambiente DATABASE_URL não encontrada")
    return url

engine = create_engine(get_database_url())

SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()