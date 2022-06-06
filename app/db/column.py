from sqlalchemy import ForeignKey, Integer, String, Date, func
from sqlalchemy import Column as Cmn
from sqlalchemy.orm import relationship
from .db import Base


class Column(Base):
    __tablename__ = "columns"
    __table_args__ = {'extend_existing': True}

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    order = Cmn(Integer)
    desk_id = Cmn(Integer, ForeignKey("desks.id", ondelete='CASCADE'), nullable=False)
    created_at = Cmn(Date, default=func.now())
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())

    desk = relationship("Desk", back_populates="columns", cascade="all, delete")
    cards = relationship("Card", back_populates="column", order_by="Card.order", cascade="all, delete")

    def __repr__(self):
        return f'Column [Id: {self.id}, title: {self.title}]'

