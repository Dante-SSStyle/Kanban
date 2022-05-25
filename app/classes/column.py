from models import ColumnCreate, ColumnExtract, ColumnExtractAll, ColumnUpdate, ColumnDelete, ColumnOrder
from db import ColumnDB, session
from sqlalchemy import func


class Column:
    @classmethod
    def extract_all(cls, column: ColumnExtractAll):
        return session.query(ColumnDB).filter(ColumnDB.desk_id == column.desk_id).order_by(ColumnDB.order).all()

    @classmethod
    def extract(cls, column: ColumnExtract):
        return session.query(ColumnDB).filter(ColumnDB.id == column.id).first()

    @classmethod
    def delete(cls, column: ColumnDelete):
        clmn = ColumnDB(id=column.id)
        fetch_column = session.query(ColumnDB).filter(ColumnDB.id == column.id).delete()
        # session.delete(fetch_column)
        session.commit()
        return clmn

    @classmethod
    def create(cls, column: ColumnCreate):
        highest_order_column = session.query(ColumnDB).\
            filter(ColumnDB.desk_id == column.desk_id).\
            order_by(ColumnDB.order.desc()).\
            first()

        highest_order = highest_order_column.order + 1 if highest_order_column and highest_order_column.order else 1

        clmn = ColumnDB(title=column.title, desk_id=column.desk_id, order=highest_order)
        session.add(clmn)
        session.commit()

        return clmn

    @classmethod
    def update(cls, column: ColumnUpdate):
        clmn = ColumnDB(id=column.id, title=column.title)

        update_body = dict(column)
        update_fields = {i: update_body[i] for i in update_body if update_body[i]}

        session.query(ColumnDB).filter(ColumnDB.id == column.id).update({**update_fields})
        session.commit()
        return clmn

    @classmethod
    def upd_order(cls, column: ColumnOrder):
        clmn1 = ColumnDB(order=column.order)
        clmn2 = ColumnDB(order=column.new_order)
        old = session.query(ColumnDB).filter(ColumnDB.order == column.order)
        new = session.query(ColumnDB).filter(ColumnDB.order == column.new_order)
        tempo = session.query(ColumnDB).filter(ColumnDB.order == 0)

        old.update({'order': 0})
        if new.all():
            new.update({'order': column.order})
            tempo.update({'order': column.new_order})
            session.commit()
        else:
            tempo.update({'order': column.order})
            session.commit()
        return clmn1, clmn2
