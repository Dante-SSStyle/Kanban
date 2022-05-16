import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from starlette.config import Config
from starlette.datastructures import Secret
from exceptions import KanbanException


try:
    config = Config(".env")
    POSTGRES_USER = config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
    POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="postgresql")
    POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
    POSTGRES_DB = config("POSTGRES_DB", cast=str)
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
# todo ловить конкретную ошибку
except Exception:
    raise KanbanException(400, 'Не найден .env файл с авторизационными данными')

database_channel = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

session = Session(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
