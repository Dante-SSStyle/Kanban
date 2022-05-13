from typing import List, Optional
from pydantic import BaseModel


class CardBase(BaseModel):
    id: int


class CardExtractAll(BaseModel):
    desk_id: int
    column_id: int = Optional


class CardExtract(CardBase):
    pass


class CardCreate(BaseModel):
    desk_id: int
    column_id: int
    title: str
    text: str = Optional
    order: int


class CardUpdate(CardBase):
    column_id: int = Optional
    estimate: int = Optional
    order: int = Optional
    text: str = Optional
    title: str = Optional


class CardDelete(CardBase):
    pass


class Card(CardBase):
    text: str
    title: str
    desk_id: int
    column_id: int
    estimate: int
    order: int
    created_at: int
    updated_at: int

    class Config:
        orm_mode = True

