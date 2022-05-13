from fastapi import APIRouter, Query
from classes import Column
from models import ColumnCreate, ColumnExtract, ColumnExtractAll, ColumnUpdate, ColumnDelete

router = APIRouter()


@router.get('/', description='Получаем столбцы доски')
async def get_all_columns(desk_id: int = Query(...)):
    return Column.extract_all(ColumnExtractAll(desk_id=desk_id))


@router.get('/{column_id}', description='Получаем конкретный столбец')
async def get_column(column_id: int):
    return Column.extract(ColumnExtract(id=column_id))


@router.post('/', description='Создаём столбец доски')
async def create_column(column: ColumnCreate):
    return Column.create(column)


@router.put('/', description='Изменяем столбец')
async def update_column(column: ColumnUpdate):
    return Column.update(column)


@router.delete('/', description='Удаляем столбец')
async def delete_column(column: ColumnDelete):
    return Column.delete(column)
