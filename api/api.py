from datetime import date

import databases
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Column, func, Integer, String, Date, ForeignKey, Text, create_engine, MetaData

with open('url.txt', 'r') as f:
    DATABASE_URL = f.readline().strip()

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

metadata = MetaData()

DeskSQL = sqlalchemy.Table(
    'desks',
    metadata,
    Column('desk_id', Integer, primary_key=True),
    Column('title', String),
    Column('create_date', Date),
    Column('update_date', Date),
    # Column('columns_in', relationship('columns', backref='desks')),
    # Column('cards_in', relationship('cards', backref='desks')),
)
ColumnSQL = sqlalchemy.Table(
            'columns',
            metadata,
            Column('column_id', Integer, primary_key=True),
            Column('title', String),
            Column('create_date', Date),
            Column('update_date', Date),
            Column('order_num', Integer, nullable=False),
            Column('desk_id', Integer, ForeignKey('desks.desk_id'), nullable=False),
            # Column('cards_in', relationship('cards', backref='columns')),
)
CardSQL = sqlalchemy.Table(
            'cards',
            metadata,
            Column('card_id', Integer, primary_key=True),
            Column('title', String),
            Column('content', Text),
            Column('create_date', Date),
            Column('update_date', Date),
            Column('end_date', Date),
            Column('order_num', Integer, nullable=False),
            Column('column_id', Integer, ForeignKey('columns.column_id'), nullable=False),
            Column('desk_id', Integer, ForeignKey('desks.desk_id'), nullable=False),
)

metadata.create_all(engine)


# class CardStructure(BaseModel):
#     card_id: int
#     title: str
#     content: str
#     create_date: date
#     update_date: date
#     end_date: date
#     column_id: int
#     desk_id: int
class JoinModule(BaseModel):
    desk_id: int
    title: str
    create_date: date
    update_date: date
    column_id: int
    title: str
    create_date: date
    update_date: date
    order_num: int
    desk_id: int


class DeskInsert(BaseModel):
    title: str


class ColumnInsert(BaseModel):
    title: str
    order_num: int
    desk_id: int


class CardInsert(BaseModel):
    title: str
    content: str
    end_date: date
    order_num: int
    column_id: int
    desk_id: int


class Desk:
    def desk_read_all(self):
        select = DeskSQL.select()
        res = database.fetch_all(select)
        return res

    def desk_read(self, desk_id):
        select = DeskSQL.select().where(DeskSQL.c.desk_id == desk_id)
        joins = select.join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.column_id)
        res = database.fetch_all(joins)
        return res


    def desk_create(self, insertion):
        query = DeskSQL.insert().values(
            title=insertion.title,
            create_date=func.now(),
            update_date=func.now(),
        )
        new = database.execute(query)
        return new

    def show_created_desk(self, new):
        new_record = DeskSQL.select().where(DeskSQL.c.desk_id == new)
        res = database.fetch_all(new_record)
        return res


class Columns:
    def column_read_all(self):
        select = ColumnSQL.select()
        res = database.fetch_all(select)
        return res

    def column_read(self, column_id):
        select = ColumnSQL.select().where(ColumnSQL.c.column_id == column_id)
        res = database.fetch_all(select)
        return res

    def column_create(self, insertion):
        query = ColumnSQL.insert().values(
            title=insertion.title,
            create_date=func.now(),
            update_date=func.now(),
            order_num=insertion.order_num,
            desk_id=insertion.desk_id
        )
        new = database.execute(query)
        return new

    def show_created_column(self, new):
        new_record = ColumnSQL.select().where(ColumnSQL.c.column_id == new)
        res = database.fetch_all(new_record)
        return res


class Card:
    def card_read_all(self):
        select = CardSQL.select()
        res = database.fetch_all(select)
        return res

    def card_read(self, card_id):
        select = CardSQL.select().where(CardSQL.c.card_id == card_id)
        res = database.fetch_all(select)
        return res

    def card_create(self, insertion):
        query = CardSQL.insert().values(
            title=insertion.title,
            content=insertion.content,
            create_date=func.now(),
            update_date=func.now(),
            end_date=insertion.end_date,
            order_num=insertion.order_num,
            column_id=insertion.column_id,
            desk_id=insertion.desk_id
        )
        new = database.execute(query)
        return new

    def show_created_card(self, new):
        new_record = CardSQL.select().where(CardSQL.c.card_id == new)
        res = database.fetch_all(new_record)
        return res
