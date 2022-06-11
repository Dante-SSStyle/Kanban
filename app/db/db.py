import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from starlette.config import Config
from starlette.datastructures import Secret
from exceptions import KanbanException
from sqlalchemy import Column as Cmn, Integer, String, Date, func, Text, ForeignKey




try:
    config = Config(".env")
    POSTGRES_USER = config("POSTGRES_USER", cast=str)
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
    POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="postgresql")
    POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
    POSTGRES_DB = config("POSTGRES_DB", cast=str)
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
except Exception:
    raise KanbanException(400, 'Не найден .env файл с авторизационными данными')

database_channel = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

session = Session(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


class Desk(Base):
    __tablename__ = "desks"
    __table_args__ = {'extend_existing': True}

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True, )
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())
    created_at = Cmn(Date, default=func.now())

    columns = relationship("Column", back_populates="desk", order_by="Column.order", cascade="all, delete")
    cards = relationship("Card", back_populates="desk", order_by="Card.order", cascade="all, delete")

    def __repr__(self):
        return f'Desk [Id: {self.id}, title: {self.title}]'


class Column(Base):
    __tablename__ = "columns"
    __table_args__ = {'extend_existing': True}

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    order = Cmn(Integer)
    desk_id = Cmn(Integer, ForeignKey("desks.id", ondelete='CASCADE'), nullable=False)
    created_at = Cmn(Date, default=func.now())
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())

    desk = relationship("Desk", back_populates="columns", cascade="all, delete")
    cards = relationship("Card", back_populates="column", order_by="Card.order", cascade="all, delete")

    def __repr__(self):
        return f'Column [Id: {self.id}, title: {self.title}]'


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = {'extend_existing': True}

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    text = Cmn(Text)
    order = Cmn(Integer)
    estimate = Cmn(Date)
    column_id = Cmn(Integer, ForeignKey("columns.id", ondelete='CASCADE'), nullable=False)
    desk_id = Cmn(Integer, ForeignKey("desks.id", ondelete='CASCADE'), nullable=False)
    created_at = Cmn(Date, default=func.now())
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())

    desk = relationship("Desk", back_populates="cards", cascade="all, delete")
    column = relationship("Column", back_populates="cards", cascade="all, delete")

    def __repr__(self):
        return f'Card [Id: {self.id}, title: {self.title}]'


Base.metadata.create_all(bind=engine)
