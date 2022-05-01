from typing import List
from fastapi import APIRouter
from classes import Columns
from models import ColumnInsert, ColumnUpdate, ColumnBase, ColumnFull

router = APIRouter()


@router.get('/all', response_model=List[ColumnBase], description='Получаем столбцы доски')
async def get_all_columns():
    column = Columns()
    res = await column.column_read_all()
    return res


@router.get('/', response_model=List[ColumnFull], description='Получаем конкретный столбец')
async def get_card(column_id: int):
    column = Columns()
    res = column.column_read(column_id)
    return res


@router.post('/', response_model=List[ColumnBase], description='Создаём столбец доски')
async def create_column(insertion: ColumnInsert):
    column = Columns()
    await column.column_create(insertion)
    res = await column.show_created(insertion)
    return res


@router.put('/', response_model=List[ColumnBase], description='Изменяем столбец')
async def update_column(column_id: int, insertion: ColumnUpdate):
    column = Columns()
    await column.column_update(column_id, insertion)
    res = await column.show_created(insertion, column_id)
    return res


@router.delete('/', response_model=List[ColumnBase], description='Удаляем столбец')
async def delete_column(column_id: int):
    column = Columns()
    res = await column.fetch_line(column_id)
    await column.column_delete(column_id)
    return res
