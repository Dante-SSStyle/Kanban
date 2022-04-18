from datetime import date

from pydantic import BaseModel


class DeskInsert(BaseModel):
    title: str


class ColumnInsert(BaseModel):
    title: str
    order_num: int
    desk_id: int


class ColumnUpdate(BaseModel):
    title: str
    order_num: int


class CardInsert(BaseModel):
    title: str
    content: str
    end_date: date = None
    order_num: int
    column_id: int
    desk_id: int


class CardUpdate(BaseModel):
    title: str
    content: str
    end_date: date
    order_num: int
    column_id: int