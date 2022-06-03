from classes import CommonClass
from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete
from db import DeskDB, session


class Desk(CommonClass):

    @classmethod
    def create(cls, desk: DeskCreate):
        dsk = DeskDB(title=desk.title)
        cls._check(dsk)
        session.add(dsk)
        session.commit()
        print(dsk)
        return dsk

    @classmethod
    def delete(cls, desk: DeskDelete):
        dsk = DeskDB(id=desk.id)
        cls._check(dsk)
        session.query(DeskDB).filter(DeskDB.id == desk.id).delete()
        session.commit()
        return dsk

    @classmethod
    def extract_all(cls):
        dsks = session.query(DeskDB).order_by(DeskDB.id).all()
        return cls._check(dsks)


    @classmethod
    def extract(cls, desk: DeskExtract, only_desk: bool = True):
        dsk = session.query(DeskDB).filter(DeskDB.id == desk.id).first()
        cls._check404(dsk)
        cls._check(dsk)

        if only_desk:
            cls._check(dsk)
            return cls._check404(dsk)

        clmns = dsk.columns
        fst_clmn = clmns[0].order
        lst_clmn = clmns[-1].order
        return {'desk': dsk, 'columns': clmns, 'first_column': fst_clmn, 'last_column': lst_clmn}

    @classmethod
    def update(cls, desk: DeskUpdate):
        dsk = DeskDB(id=desk.id, title=desk.title)
        cls._check(dsk)
        upd = session.query(DeskDB).filter(DeskDB.id == desk.id).update({DeskDB.title: desk.title})
        cls._check(upd)
        session.commit()
        return dsk
