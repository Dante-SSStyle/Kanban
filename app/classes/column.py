from sqlalchemy.orm import Session
from models import ColumnCreate, ColumnExtract, ColumnExtractAll, ColumnUpdate, ColumnDelete
from db import ColumnDB


class Column:
    def __init__(self, db: Session):
        self.db = db

    def extract_all(self, column: ColumnExtractAll):
        return self.db.query(ColumnDB).filter(ColumnDB.desk_id == column.desk_id).all()

    def extract(self, column: ColumnExtract):
        return self.db.query(ColumnDB).filter(ColumnDB.id == column.id).first()

    def create(self, column: ColumnCreate):
        dsk = ColumnDB(title=column.title, desk_id=column.desk_id)
        self.db.add(dsk)
        self.db.commit()
        self.db.refresh(dsk)
        return dsk

    def delete(self, column: ColumnDelete):
        dsk = ColumnDB(id=column.id)
        self.db.delete(dsk)
