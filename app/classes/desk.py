from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete
from db import DeskDB, ColumnDB, session


class Desk:

    @classmethod
    def create(cls, desk: DeskCreate):
        dsk = DeskDB(title=desk.title)
        session.add(dsk)
        session.commit()
        return dsk

    @classmethod
    def delete(cls, desk: DeskDelete):
        dsk = DeskDB(id=desk.id)
        session.query(DeskDB).filter(DeskDB.id == desk.id).delete()
        session.commit()
        return dsk

    @classmethod
    def extract_all(cls):
        return session.query(DeskDB).order_by(DeskDB.id).all()

    @classmethod
    def extract(cls, desk: DeskExtract, only_desk: bool = True):
        dsk = session.query(DeskDB).filter(DeskDB.id == desk.id).first()

        if only_desk:
            return dsk

        clmns = dsk.columns
        return {'desk': dsk, 'columns': clmns}

    @classmethod
    def update(cls, desk: DeskUpdate):
        dsk = DeskDB(id=desk.id, title=desk.title)
        session.query(DeskDB).filter(DeskDB.id == desk.id).update({DeskDB.title: desk.title})
        session.commit()
        return dsk
