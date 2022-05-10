from typing import List, Optional
from pydantic import BaseModel


class CardBase(BaseModel):
    title: str
    desk_id: int
    column_id: int


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int
    is_active: bool
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True


class ColumnBase(BaseModel):
    title: str
    desk_id: int


class ColumnCreate(ColumnBase):
    pass


class Column(ColumnBase):
    id: int
    is_active: bool
    cards: List[Card] = []
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True


class DeskBase(BaseModel):
    title: str


class DeskCreate(DeskBase):
    pass


class Desk(DeskBase):
    id: int
    columns: List[Column] = []
    cards: List[Card] = []
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True


