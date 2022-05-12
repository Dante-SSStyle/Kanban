# from sqlalchemy.orm import Session
from models import DeskCreate, DeskExtract, DeskExtractAll, DeskUpdate, DeskDelete
from db import DeskDB, session


class Desk:

    @classmethod
    def create(cls, desk: DeskCreate):
        dsk = DeskDB(title=desk.title)
        session.add(dsk)
        session.commit()
        session.refresh(dsk)
        return dsk

    @classmethod
    def delete(cls, desk: DeskDelete):
        dsk = DeskDB(id=desk.id)
        session.query(DeskDB).filter(DeskDB.id == desk.id).delete()
        return dsk

    @classmethod
    def extract_all(cls):
        return session.query(DeskDB).order_by(DeskDB.id).all()

    @classmethod
    def extract(cls, desk: DeskExtract):
        return session.query(DeskDB).filter(DeskDB.id == desk.id).first()

    @classmethod
    def update(cls, desk: DeskUpdate):
        dsk = DeskDB(id=desk.id, title=desk.title)
        session.query(DeskDB).filter(DeskDB.id == desk.id).update({DeskDB.title: desk.title})
        return dsk
