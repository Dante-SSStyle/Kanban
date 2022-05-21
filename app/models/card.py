from datetime import date
from typing import List, Optional
from pydantic import BaseModel


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
    title: str
    text: Optional[str] = "Empty"


class CardUpdate(CardBase):
    column_id: Optional[int] = None
    estimate: Optional[date] = None
    # order: Optional[int] = None
    text: Optional[str] = None
    title: Optional[str] = None


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

