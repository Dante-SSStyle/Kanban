from sqlalchemy import Column as Cmn, Integer, String, Date, func
from sqlalchemy.orm import relationship
from .db import Base


class Desk(Base):
    __tablename__ = "desks"
    __table_args__ = {'extend_existing': True}

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True, )
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())
    created_at = Cmn(Date, default=func.now())

    columns = relationship("Column", back_populates="desk", order_by="Column.order", cascade="all, delete")
    cards = relationship("Card", back_populates="desk", order_by="Card.order", cascade="all, delete")

    def __repr__(self):
        return f'Desk [Id: {self.id}, title: {self.title}]'
