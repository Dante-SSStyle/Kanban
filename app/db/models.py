from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, Date, func
from sqlalchemy import Column as Cmn
from sqlalchemy.orm import relationship

from .db import Base


class Column(Base):
    __tablename__ = "columns"

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    order = Cmn(Integer)
    desk_id = Cmn(Integer, ForeignKey("desks.id"), nullable=False)
    created_at = Cmn(Date, default=func.now())
    updated_at = Cmn(Date, default=func.now())

    desk = relationship("Desk", back_populates="columns")
    cards = relationship("Card", back_populates="column")

    def __repr__(self):
        return f'Column [Id: {self.id}, title: {self.title}]'


class Card(Base):
    __tablename__ = "cards"

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    text = Cmn(Text)
    order = Cmn(Integer)
    estimate = Cmn(Date)
    column_id = Cmn(Integer, ForeignKey("columns.id"), nullable=False)
    desk_id = Cmn(Integer, ForeignKey("desks.id"), nullable=False)
    created_at = Cmn(Date, default=func.now())
    updated_at = Cmn(Date, default=func.now())

    desk = relationship("Desk", back_populates="cards")
    column = relationship("Column", back_populates="cards")

    def __repr__(self):
        return f'Card [Id: {self.id}, title: {self.title}]'


class Desk(Base):
    __tablename__ = "desks"

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    updated_at = Cmn(Date, default=func.now())
    created_at = Cmn(Date, default=func.now())

    columns = relationship("Column", back_populates="desk")
    cards = relationship("Card", back_populates="desk")

    def __repr__(self):
        return f'Desk [Id: {self.id}, title: {self.title}]'
