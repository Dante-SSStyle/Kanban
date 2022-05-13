from typing import List, Optional
from pydantic import BaseModel
from .card import Card


class ColumnBase(BaseModel):
    id: int


class ColumnExtractAll(BaseModel):
    desk_id: int


class ColumnExtract(ColumnBase):
    pass


class ColumnCreate(BaseModel):
    desk_id: int
    title: str
    order: int = Optional


class ColumnUpdate(ColumnBase):
    title: str = Optional
    order: int = Optional


class ColumnDelete(ColumnBase):
    pass


class Column(ColumnBase):
    id: int
    title: str
    desk_id: int
    order: int
    cards: List[Card] = []
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True

