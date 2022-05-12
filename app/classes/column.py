from sqlalchemy.orm import Session
from models import ColumnCreate, ColumnExtract, ColumnExtractAll, ColumnUpdate, ColumnDelete
from db import ColumnDB, session


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
        session.query(ColumnDB).filter(ColumnDB.id == column.id).delete()
        return clmn

    @classmethod
    def create(cls, column: ColumnCreate):
        clmn = ColumnDB(title=column.title, desk_id=column.desk_id)
        session.add(clmn)
        session.commit()
        session.refresh(clmn)
        return clmn

    @classmethod
    def update(cls, column: ColumnUpdate):
        clmn = ColumnDB(id=column.id, title=column.title)
        session.query(ColumnDB).filter(ColumnDB.id == column.id).update({ColumnDB.title: column.title})
        return clmn
