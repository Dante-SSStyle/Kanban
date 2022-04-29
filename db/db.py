import os
import databases
import sqlalchemy
from sqlalchemy import Column, func, Integer, String, Date, ForeignKey, Text, create_engine, MetaData
from sqlalchemy.orm import Session
from exceptions.exceptions import KanbanException


if not os.path.exists('db/url.txt'):
    raise KanbanException(400, 'Не найден файл с url базы данных')

with open('db/url.txt', 'r') as f:
    DATABASE_URL = f.readline().strip()

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
session = Session(bind=engine)

metadata = MetaData()
DeskSQL = sqlalchemy.Table(
    'desks',
    metadata,
    Column('desk_id', Integer, primary_key=True),
    Column('desk_title', String, nullable=False, unique=True),
    Column('desk_create_date', Date, default=func.now(), nullable=False),
    Column('desk_update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
)
ColumnSQL = sqlalchemy.Table(
    'columns',
    metadata,
    Column('column_id', Integer, primary_key=True),
    Column('column_title', String, nullable=False, unique=True),
    Column('column_create_date', Date, default=func.now(), nullable=False),
    Column('column_update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
    Column('column_order_num', Integer, nullable=False),
    Column('desk_id', Integer, ForeignKey('desks.desk_id', ondelete="CASCADE"), nullable=False),
)
CardSQL = sqlalchemy.Table(
    'cards',
    metadata,
    Column('card_id', Integer, primary_key=True),
    Column('card_title', String, nullable=False, unique=True),
    Column('content', Text, nullable=True),
    Column('card_create_date', Date, default=func.now(), nullable=False),
    Column('card_update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
    Column('end_date', Date, default=None, nullable=True),
    Column('card_order_num', Integer, nullable=False),
    Column('column_id', Integer, ForeignKey('columns.column_id', ondelete="CASCADE"), nullable=False),
    Column('desk_id', Integer, ForeignKey('desks.desk_id', ondelete="CASCADE"), nullable=False),
)

metadata.create_all(engine)
