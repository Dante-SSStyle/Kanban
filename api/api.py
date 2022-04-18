import os
import databases
import sqlalchemy
from sqlalchemy import Column, func, Integer, String, Date, ForeignKey, Text, create_engine, MetaData, CheckConstraint
from sqlalchemy.orm import Session
from api.exceptions import KanbanException


if not os.path.exists('api/url.txt'):
    raise KanbanException(400, 'Не найден файл с url базы данных')

with open('api/url.txt', 'r') as f:
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
            Column('column_order_num', Integer, CheckConstraint('column_order_num>0'), nullable=False),
            Column('desk_id', Integer, ForeignKey('desks.desk_id', ondelete="CASCADE"), nullable=False),
)
CardSQL = sqlalchemy.Table(
            'cards',
            metadata,
            Column('card_id', Integer, primary_key=True),
            Column('card_title', String, nullable=False, unique=True),
            Column('content', Text, nullable=False),
            Column('card_create_date', Date, default=func.now(), nullable=False),
            Column('card_update_date', Date, default=func.now(), onupdate=func.now(), nullable=False),
            Column('end_date', Date, default=None, nullable=True),
            Column('card_order_num', Integer, CheckConstraint('card_order_num>0'), nullable=False),
            Column('column_id', Integer, ForeignKey('columns.column_id', ondelete="CASCADE"), nullable=False),
            Column('desk_id', Integer, ForeignKey('desks.desk_id', ondelete="CASCADE"), nullable=False),
)

metadata.create_all(engine)


class MainInnerClass:
    def __init__(self):
        pass
    '''Проверка данных перед использованием JOIN для вывода полной информации о столбцах/доске'''
    def _c_check_res(self, res, column_id):
        if not res:
            return session.query(ColumnSQL).filter(ColumnSQL.c.column_id == column_id).all()
        return res

    def _d_check_res(self, res, desk_id):
        if not session.query(DeskSQL, ColumnSQL).join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id).all():
            return session.query(DeskSQL).filter(DeskSQL.c.desk_id == desk_id).all()
        if not res:
            return session.query(DeskSQL, ColumnSQL).join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id)\
                .filter(DeskSQL.c.desk_id == desk_id).all()
        return res
    '''Проверка упорядоченности для столбца/карточки (два столбца не могут занимать одну позицию на доске)'''
    def _col_check_order(self, insertion):
        query = session.query(ColumnSQL).all()
        for line in query:
            if line[4] == insertion.order_num and line[5] == insertion.desk_id:
                raise KanbanException(400, 'Неверный указатель позиции столбца на доске')

    def _car_check_order(self, insertion):
        query = session.query(CardSQL).all()
        for line in query:
            if line[6] == insertion.order_num and line[7] == insertion.column_id and line[8] == insertion.desk_id:
                raise KanbanException(400, 'Неверный указатель позиции карточки')


class Desk(MainInnerClass):
    def __init__(self):
        super().__init__()

    def desk_read_all(self):
        select = DeskSQL.select()
        res = database.fetch_all(select)
        return res

    def desk_read(self, desk_id: int):
        join = session.query(DeskSQL, ColumnSQL, CardSQL).join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id)
        res = join.join(CardSQL, ColumnSQL.c.column_id == CardSQL.c.column_id).filter(DeskSQL.c.desk_id == desk_id).all()
        result = self._d_check_res(res, desk_id)
        return result


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


class Columns(MainInnerClass):
    def __init__(self):
        super().__init__()

    def column_read_all(self):
        select = ColumnSQL.select()
        res = database.fetch_all(select)
        return res

    def column_read(self, column_id: int):
        join = session.query(ColumnSQL, CardSQL).join(CardSQL, ColumnSQL.c.column_id == CardSQL.c.column_id)
        res = join.filter(ColumnSQL.c.column_id == column_id).all()
        result = self._c_check_res(res, column_id)
        return result

    def column_create(self, insertion):
        query = ColumnSQL.insert().values(
            column_title=insertion.title,
            column_order_num=insertion.order_num,
            desk_id=insertion.desk_id
        )
        self._col_check_order(insertion)
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


class Card(MainInnerClass):
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
        self._car_check_order(insertion)
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
