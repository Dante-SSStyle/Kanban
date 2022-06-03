from classes import CommonClass
from models import CardCreate, CardDelete, CardExtract, CardExtractAll, CardUpdate, CardOrder
from db import CardDB, ColumnDB, session


class Card(CommonClass):

    @classmethod
    def extract_all(cls, card: CardExtractAll):
        cards = session.query(CardDB).filter(CardDB.desk_id == card.desk_id,
                                            CardDB.column_id == card.column_id).order_by(CardDB.order).all()
        return cls._check(cards)

    @classmethod
    def extract(cls, card: CardExtract, only_card: bool = True):
        crd = session.query(CardDB).filter(CardDB.id == card.id).first()
        cls._check404(crd)
        cls._check(crd)

        if only_card:
            cls._check(crd)
            return cls._check404(crd)
        clmns = session.query(ColumnDB).filter(ColumnDB.desk_id == crd.desk_id).all()
        return {'card': crd, 'columns': clmns}

    @classmethod
    def delete(cls, card: CardDelete):
        crd = CardDB(id=card.id)
        cls._check(crd)
        session.query(CardDB).filter(CardDB.id == card.id).delete()
        session.commit()
        return crd

    @classmethod
    def create(cls, card: CardCreate):
        highest_order_card = session.query(CardDB). \
            filter(CardDB.desk_id == card.desk_id, CardDB.column_id == card.column_id). \
            order_by(CardDB.order.desc()). \
            first()

        highest_order = highest_order_card.order + 1 if highest_order_card and highest_order_card.order else 1

        crd = CardDB(title=card.title, text=card.text, desk_id=card.desk_id, column_id=card.column_id,
                     order=highest_order)
        cls._check(crd)
        session.add(crd)
        session.commit()

        return crd

    @classmethod
    def update(cls, card: CardUpdate):
        crd = CardDB(id=card.id, title=card.title, text=card.text, column_id=card.column_id, estimate=card.estimate)

        cls._check(crd)
        update_body = dict(card)
        update_fields = {i: update_body[i] for i in update_body if update_body[i]}

        upd = session.query(CardDB).filter(CardDB.id == card.id).update({**update_fields})
        cls._check(upd)
        session.commit()
        return crd

    @classmethod
    def upd_order(cls, card: CardOrder):
        crd1 = CardDB(order=card.order)
        crd2 = CardDB(order=card.new_order)

        old = session.query(CardDB).filter(CardDB.order == card.order)
        new = session.query(CardDB).filter(CardDB.order == card.new_order)
        tempo = session.query(CardDB).filter(CardDB.order == 0)

        old.update({'order': 0})
        if new.all():
            new.update({'order': card.order})
            tempo.update({'order': card.new_order})
            session.commit()
        else:
            tempo.update({'order': card.order})
            session.commit()
        return crd1, crd2
