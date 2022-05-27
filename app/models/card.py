from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class CardBase(BaseModel):
    id: int


class CardExtractAll(BaseModel):
    desk_id: int
    column_id: Optional[int] = None


class CardExtract(CardBase):
    pass


class CardCreate(BaseModel):
    desk_id: int
    column_id: int
    title: str = Field(min_length=1, max_length=50)
    text: Optional[str] = Field(max_length=1000, default='Пусто', )


class CardUpdate(CardBase):
    column_id: Optional[int] = None
    estimate: Optional[date] = None
    # order: Optional[int] = None
    text: Optional[str] = Field(max_length=1000)
    title: str = Field(min_length=1, max_length=50)


class CardDelete(CardBase):
    pass


class CardOrder(CardBase):
    order: int
    new_order: int


class Card(CardBase):
    text: str = Field(max_length=1000)
    title: str = Field(min_length=1, max_length=50)
    desk_id: int
    column_id: int
    estimate: int
    order: int
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True

