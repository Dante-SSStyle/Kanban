from typing import List, Optional
from pydantic import BaseModel, Field
from .card import Card


class ColumnBase(BaseModel):
    id: int


class ColumnExtractAll(BaseModel):
    desk_id: int


class ColumnExtract(ColumnBase):
    pass


class ColumnCreate(BaseModel):
    desk_id: int
    title: str = Field(min_length=1, max_length=50)


class ColumnUpdate(ColumnBase):
    title: str = Field(min_length=1, max_length=50)


class ColumnDelete(ColumnBase):
    pass

class ColumnOrder(ColumnBase):
    order: int
    new_order: int

class Column(ColumnBase):
    id: int
    title: str = Field(min_length=1, max_length=50)
    desk_id: int
    order: int
    cards: List[Card] = []
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True

