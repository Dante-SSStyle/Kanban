# import databases
# import sqlalchemy
# from sqlalchemy import Column, func, Integer, String, Date, ForeignKey, Text, create_engine, MetaData
# from sqlalchemy.orm import Session
# from starlette.config import Config
# from starlette.datastructures import Secret
# from exceptions import KanbanException
#
# try:
#     config = Config(".env")
#     POSTGRES_USER = config("POSTGRES_USER", cast=str)
#     POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
#     POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="postgresql")
#     POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
#     POSTGRES_DB = config("POSTGRES_DB", cast=str)
#     DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
# # todo ловить конкретную ошибку
# except Exception:
#     raise KanbanException(400, 'Не найден .env файл с авторизационными данными')
#
# database = databases.Database(DATABASE_URL)
# engine = create_engine(DATABASE_URL)
# session = Session(bind=engine)
#
# metadata = MetaData()
# DeskSQL = sqlalchemy.Table(
#     'desks',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('title', String, nullable=False, unique=True),
#     Column('create_date', Date, default=func.now(), nullable=False),
#     Column('update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
# )
# ColumnSQL = sqlalchemy.Table(
#     'columns',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('title', String, nullable=False, unique=True),
#     Column('create_date', Date, default=func.now(), nullable=False),
#     Column('update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
#     Column('order_num', Integer, nullable=False),
#     Column('desk_id', Integer, ForeignKey('desks.id', ondelete="CASCADE"), nullable=False),
# )
# CardSQL = sqlalchemy.Table(
#     'cards',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('title', String, nullable=False, unique=True),
#     Column('content', Text, nullable=True),
#     Column('create_date', Date, default=func.now(), nullable=False),
#     Column('update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
#     Column('end_date', Date, default=None, nullable=True),
#     Column('order_num', Integer, nullable=False),
#     Column('column_id', Integer, ForeignKey('columns.id', ondelete="CASCADE"), nullable=False),
#     Column('desk_id', Integer, ForeignKey('desks.id', ondelete="CASCADE"), nullable=False),
# )
#
# metadata.create_all(engine)
