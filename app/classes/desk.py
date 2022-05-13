from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete
from db import DeskDB, session


class Desk:

    @classmethod
    def _sort_cards(cls, desk, columns, cards):
        tmp = []
        for i in columns:
            # i['cards'] = [c for c in cards if c['column_id'] == i['id']]
            tmp.append(i.cards)

        return {'desk': desk, 'columns': columns, 'cards': tmp}

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
        dsk = session.query(DeskDB).filter(DeskDB.id == desk.id).first()
        clmns = dsk.columns
        # crds = dsk.cards
        # return cls._sort_cards(dsk, clmns, crds)
        return {'desk': dsk, 'columns': clmns}

    @classmethod
    def update(cls, desk: DeskUpdate):
        dsk = DeskDB(id=desk.id, title=desk.title)
        session.query(DeskDB).filter(DeskDB.id == desk.id).update({DeskDB.title: desk.title})
        return dsk
