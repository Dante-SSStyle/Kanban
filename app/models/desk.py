from typing import List
from pydantic import BaseModel, Field
from .card import Card
from .column import Column


class DeskBase(BaseModel):
    id: int


class DeskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)


class DeskExtractAll(BaseModel):
    pass


class DeskExtract(DeskBase):
    pass


class DeskUpdate(DeskBase):
    title: str = Field(min_length=3, max_length=50)


class DeskDelete(DeskBase):
    pass


class Desk(DeskBase):
    id: int
    title: str = Field(min_length=3, max_length=50)
    columns: List[Column] = []
    cards: List[Card] = []
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True
