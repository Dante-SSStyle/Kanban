from typing import List, Optional
from pydantic import BaseModel
from .card import Card
from .column import Column


class DeskBase(BaseModel):
    id: int


class DeskCreate(BaseModel):
    title: str


class DeskExtractAll(BaseModel):
    pass


class DeskExtract(DeskBase):
    pass


class DeskUpdate(DeskBase):
    title: str


class DeskDelete(DeskBase):
    pass


class Desk(DeskBase):
    id: int
    title: str
    columns: List[Column] = []
    cards: List[Card] = []
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True
