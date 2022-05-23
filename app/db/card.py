from sqlalchemy import Boolean, Column as Cmn, ForeignKey, Integer, String, Text, Date, func
from sqlalchemy.orm import relationship
from .db import Base


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = {'extend_existing': True}

    id = Cmn(Integer, primary_key=True, index=True)
    title = Cmn(String, index=True)
    text = Cmn(Text)
    order = Cmn(Integer)
    estimate = Cmn(Date)
    column_id = Cmn(Integer, ForeignKey("columns.id"), nullable=False)
    desk_id = Cmn(Integer, ForeignKey("desks.id"), nullable=False)
    created_at = Cmn(Date, default=func.now())
    updated_at = Cmn(Date, default=func.now(), onupdate=func.now())

    desk = relationship("Desk", back_populates="cards")
    column = relationship("Column", back_populates="cards")

    def __repr__(self):
        return f'Card [Id: {self.id}, title: {self.title}]'
