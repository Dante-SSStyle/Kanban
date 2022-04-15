from datetime import date

import databases
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Column, func, Integer, String, Date, ForeignKey, Text, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/Test'
# database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

metadata = MetaData()
Base = declarative_base()


class DeskSQL(Base):
    __tablename__ = 'desks'
    desk_id = Column(Integer, primary_key=True)
    title = Column(String)
    create_date = Column(Date)
    update_date = Column(Date)
    columns_in = relationship('ColumnSQL', backref='desks')
    cards_in = relationship('CardSQL', backref='desks')


# DeskSQL = sqlalchemy.Table(
#     'desks',
#     metadata,
#     Column('desk_id', Integer, primary_key=True),
#     Column('title', String),
#     Column('create_date', Date),
#     Column('update_date', Date),
#     Column('columns_in', relationship('columns', backref='desks')),
#     Column('cards_in', relationship('cards', backref='desks')),
# )
class ColumnSQL(Base):
    __tablename__ = 'columns'
    column_id = Column(Integer, primary_key=True)
    title = Column(String)
    create_date = Column(Date)
    update_date = Column(Date)
    order_num = Column(Integer, nullable=False)
    desk_id = Column(Integer, ForeignKey('desks.desk_id'), nullable=False)
    cards_in = relationship('CardSQL', backref='columns')


# ColumnSQL = sqlalchemy.Table(
#             'columns',
#             metadata,
#             Column('column_id', Integer, primary_key=True),
#             Column('title', String),
#             Column('create_date', Date),
#             Column('update_date', Date),
#             Column('order_num', Integer, nullable=False),
#             Column('desk_id', Integer, ForeignKey('desks.desk_id'), nullable=False),
#             Column('cards_in', relationship('cards', backref='columns')),
# )
class CardSQL(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    create_date = Column(Date)
    update_date = Column(Date)
    end_date = Column(Date)
    order_num = Column(Integer, nullable=False)
    desk_id = Column(Integer, ForeignKey('desks.desk_id'), nullable=False)
    column_id = Column(Integer, ForeignKey('columns.column_id'), nullable=False)


# CardSQL = sqlalchemy.Table(
#             'cards',
#             metadata,
#             Column('card_id', Integer, primary_key=True),
#             Column('title', String),
#             Column('content', Text),
#             Column('create_date', Date),
#             Column('update_date', Date),
#             Column('end_date', Date),
#             Column('order_num', Integer, nullable=False),
#             Column('column_id', Integer, ForeignKey('columns.column_id'), nullable=False),
#             Column('desk_id', Integer, ForeignKey('desks.desk_id'), nullable=False),
# )

# engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



# class CardStructure(BaseModel):
#     card_id: int
#     title: str
#     content: str
#     create_date: date
#     update_date: date
#     end_date: date
#     column_id: int
#     desk_id: int


class CardInsert(BaseModel):
    title: str
    content: str
    end_date: date
    order_num: int
    column_id: int
    desk_id: int


class ColumnInsert(BaseModel):
    title: str
    order_num: int
    desk_id: int


# class Desk:
#     def desk_read(self):
#         select = DeskSQL.select()
#         res = database.fetch_all(select)
#         return res

class Desk:
    def desk_read(self):
        select = session.query(DeskSQL)
        # res = database.fetch_all(select)
        return select


# class Columns:
#     def column_read_all(self):
#         select = ColumnSQL.select()
#         res = database.fetch_all(select)
#         return res
#
#     def column_create(self, insertion):
#         query = ColumnSQL.insert().values(
#             title=insertion.title,
#             create_date=func.now(),
#             update_date=func.now(),
#             order_num=insertion.order_num,
#             desk_id=insertion.desk_id
#         )
#         new = database.execute(query)
#         return new
#
#     def show_created_column(self, new):
#         new_record = ColumnSQL.select().where(ColumnSQL.c.card_id == new)
#         res = database.fetch_all(new_record)
#         return res
#
#
# class Card:
#     def card_read_all(self):
#         select = CardSQL.select()
#         res = database.fetch_all(select)
#         return res
#
#     def card_read(self, card_id):
#         select = CardSQL.select().where(CardSQL.c.card_id == card_id)
#         res = database.fetch_all(select)
#         return res
#
#     def card_create(self, insertion):
#         query = CardSQL.insert().values(
#             title=insertion.title,
#             content=insertion.content,
#             create_date=func.now(),
#             update_date=func.now(),
#             end_date=insertion.end_date,
#             order_num=insertion.order_num,
#             column_id=insertion.column_id,
#             desk_id=insertion.desk_id
#         )
#         new = database.execute(query)
#         return new
#
#     def show_created_card(self, new):
#         new_record = CardSQL.select().where(CardSQL.c.card_id == new)
#         res = database.fetch_all(new_record)
#         return res
