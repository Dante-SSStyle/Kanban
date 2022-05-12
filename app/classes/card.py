from sqlalchemy.orm import Session
from models import CardCreate, CardDelete, CardExtract, CardExtractAll, CardUpdate
from db import CardDB, session


class Card:

    @classmethod
    def extract_all(cls, card: CardExtractAll):
        return session.query(CardDB).filter(CardDB.desk_id == card.desk_id).order_by(CardDB.order).all()

    @classmethod
    def extract(cls, card: CardExtract):
        return session.query(CardDB).filter(CardDB.id == card.id).first()

    @classmethod
    def delete(cls, card: CardDelete):
        crd = CardDB(id=card.id)
        session.query(CardDB).filter(CardDB.id == card.id).delete()
        return crd

    @classmethod
    def create(cls, card: CardCreate):
        crd = CardDB(title=card.title, text=card.text)
        session.add(crd)
        session.commit()
        session.refresh(crd)
        return crd

    @classmethod
    def update(cls, card: CardUpdate):
        crd = CardDB(id=card.id, title=card.title, text=card.text)
        session.query(CardDB).filter(CardDB.id == card.id).update({CardDB.title: card.title, CardDB.text: card.text})
        return crd
