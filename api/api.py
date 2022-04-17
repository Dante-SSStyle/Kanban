import databases
import sqlalchemy
from sqlalchemy import Column, func, Integer, String, Date, ForeignKey, Text, create_engine, MetaData
from sqlalchemy.orm import Session

with open('url.txt', 'r') as f:
    DATABASE_URL = f.readline().strip()

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
session = Session(bind=engine)

metadata = MetaData()
DeskSQL = sqlalchemy.Table(
    'desks',
    metadata,
    Column('desk_id', Integer, primary_key=True),
    Column('desk_title', String),
    Column('desk_create_date', Date, default=func.now()),
    Column('desk_update_date', Date, default=func.now()),
)
ColumnSQL = sqlalchemy.Table(
            'columns',
            metadata,
            Column('column_id', Integer, primary_key=True),
            Column('column_title', String),
            Column('column_create_date', Date, default=func.now()),
            Column('column_update_date', Date, default=func.now()),
            Column('column_order_num', Integer, nullable=False),
            Column('desk_id', Integer, ForeignKey('desks.desk_id'), nullable=False),
)
CardSQL = sqlalchemy.Table(
            'cards',
            metadata,
            Column('card_id', Integer, primary_key=True),
            Column('card_title', String),
            Column('content', Text, nullable=False),
            Column('card_create_date', Date, default=func.now()),
            Column('card_update_date', Date, default=func.now()),
            Column('end_date', Date),
            Column('card_order_num', Integer, nullable=False),
            Column('column_id', Integer, ForeignKey('columns.column_id'), nullable=False),
            Column('desk_id', Integer, ForeignKey('desks.desk_id'), nullable=False),
)

metadata.create_all(engine)


class Desk:
    def desk_read_all(self):
        select = DeskSQL.select()
        res = database.fetch_all(select)
        return res

    def desk_read(self, desk_id: int):
        join = session.query(DeskSQL, ColumnSQL, CardSQL).join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id)
        res = join.join(CardSQL, ColumnSQL.c.column_id == CardSQL.c.column_id).filter(DeskSQL.c.desk_id == desk_id).all()
        return res

    def desk_create(self, insertion):
        query = DeskSQL.insert().values(
            desk_title=insertion.title
        )
        new = database.execute(query)
        return new

    def show_created(self, new):
        new_record = DeskSQL.select().where(DeskSQL.c.desk_id == new)
        res = database.fetch_all(new_record)
        return res

    def desk_update(self, desk_id: int, insertion):
        query = DeskSQL.update().where(DeskSQL.c.desk_id == desk_id).values(
            desk_title=insertion.title
        )
        res = database.execute(query)
        return res

    def desk_delete(self, desk_id: int):
        query = DeskSQL.delete().where(DeskSQL.c.desk_id == desk_id)
        res = database.execute(query)
        return res

    def show_deleted(self, desk_id: int):
        deleted_record = DeskSQL.select().where(DeskSQL.c.desk_id == desk_id)
        res = database.fetch_all(deleted_record)
        return res


class Columns:
    def column_read_all(self):
        select = ColumnSQL.select()
        res = database.fetch_all(select)
        return res

    def column_read(self, column_id: int):
        select = ColumnSQL.select().where(ColumnSQL.c.column_id == column_id)
        res = database.fetch_all(select)
        return res

    def column_create(self, insertion):
        query = ColumnSQL.insert().values(
            column_title=insertion.title,
            column_order_num=insertion.order_num,
            desk_id=insertion.desk_id
        )
        new = database.execute(query)
        return new

    def show_created(self, new):
        new_record = ColumnSQL.select().where(ColumnSQL.c.column_id == new)
        res = database.fetch_all(new_record)
        return res

    def column_update(self, column_id: int, insertion):
        query = ColumnSQL.update().where(ColumnSQL.c.column_id == column_id).values(
            column_title=insertion.title,
            column_order_num=insertion.order_num
        )
        res = database.execute(query)
        return res

    def column_delete(self, column_id: int):
        query = ColumnSQL.delete().where(ColumnSQL.c.column_id == column_id)
        res = database.execute(query)
        return res

    def show_deleted(self, column_id: int):
        deleted_record = ColumnSQL.select().where(ColumnSQL.c.column_id == column_id)
        res = database.fetch_all(deleted_record)
        return res


class Card:
    def card_read_all(self):
        select = CardSQL.select()
        res = database.fetch_all(select)
        return res

    def card_read(self, card_id: int):
        select = CardSQL.select().where(CardSQL.c.card_id == card_id)
        res = database.fetch_all(select)
        return res

    def card_create(self, insertion):
        query = CardSQL.insert().values(
            card_title=insertion.title,
            content=insertion.content,
            end_date=insertion.end_date,
            card_order_num=insertion.order_num,
            column_id=insertion.column_id,
            desk_id=insertion.desk_id
        )
        new = database.execute(query)
        return new

    def show_created(self, new):
        new_record = CardSQL.select().where(CardSQL.c.card_id == new)
        res = database.fetch_all(new_record)
        return res

    def card_update(self, card_id: int, insertion):
        query = CardSQL.update().where(CardSQL.c.card_id == card_id).values(
            card_title=insertion.title,
            content=insertion.content,
            end_date=insertion.end_date,
            card_order_num=insertion.order_num,
            column_id=insertion.column_id,
        )
        res = database.execute(query)
        return res

    def card_delete(self, card_id: int):
        query = CardSQL.delete().where(CardSQL.c.card_id == card_id)
        res = database.execute(query)
        return res

    def show_deleted(self, card_id: int):
        deleted_record = CardSQL.select().where(CardSQL.c.card_id == card_id)
        res = database.fetch_all(deleted_record)
        return res
