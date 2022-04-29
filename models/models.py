from datetime import date
from pydantic import BaseModel, Field


class DeskBase(BaseModel):
    desk_id: int
    desk_title: str
    desk_create_date: date
    desk_update_date: date


class DeskFull(BaseModel):
    desk_id: int = None
    desk_title: str
    desk_create_date: date
    desk_update_date: date
    column_id: int = None
    column_title: str = None
    column_create_date: date = None
    column_update_date: date = None
    column_order_num: int = None
    card_id: int = None
    card_title: str = None
    content: str = None
    card_create_date: date = None
    card_update_date: date = None
    end_date: date = None
    card_order_num: int = None


class ColumnFull(BaseModel):
    column_id: int
    column_title: str
    column_create_date: date
    column_update_date: date
    column_order_num: int
    desk_id: int
    card_id: int = None
    card_title: str = None
    content: str = None
    card_create_date: date = None
    card_update_date: date = None
    end_date: date = None
    card_order_num: int = None


class ColumnBase(BaseModel):
    column_id: int
    column_title: str
    column_create_date: date
    column_update_date: date
    column_order_num: int
    desk_id: int


class CardBase(BaseModel):
    card_id: int
    card_title: str
    content: str
    card_create_date: date
    card_update_date: date
    end_date: date = None
    card_order_num: int
    column_id: int
    desk_id: int


class DeskInsert(BaseModel):
    title: str = Field(min_length=1, max_length=30)


class ColumnInsert(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    desk_id: int


class ColumnUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    order_num: int = Field(ge=1)


class CardInsert(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    content: str = Field(min_length=0, max_length=250)
    end_date: date = None
    column_id: int
    desk_id: int


class CardUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    content: str = Field(min_length=0, max_length=250)
    end_date: date = None
    order_num: int = Field(ge=1)
    column_id: int
