from sqlalchemy import Boolean, Column as Cmn, ForeignKey, Integer, String, Text, Date, func
from sqlalchemy.orm import relationship

from .db import Base


class Desk(Base):
    __tablename__ = "desks"

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())
    created_at = Cmn(Date, default=func.now())

    columns = relationship("Column", back_populates="desk")
    cards = relationship("Card", back_populates="desk")

    def __repr__(self):
        return f'Desk [Id: {self.id}, title: {self.title}]'
