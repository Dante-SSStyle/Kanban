from sqlalchemy.orm import Session
from models import CardCreate, CardDelete, CardExtract, CardExtractAll
from db import CardDB


class Card:
    def __init__(self, db: Session):
        self.db = db

    def extract_all(self, card: CardExtractAll):
        return self.db.query(CardDB).filter(CardDB.desk_id == card.desk_id).all()

    def extract(self, card: CardExtract):
        return self.db.query(CardDB).filter(CardDB.id == card.id).first()

    def create(self, card: CardCreate):
        crd = CardDB(title=card.title, text=card.text)
        self.db.add(crd)
        self.db.commit()
        self.db.refresh(crd)
        return crd

    def delete(self, card: CardDelete):
        dsk = CardDB(id=card.id)
        self.db.delete(dsk)
