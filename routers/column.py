from fastapi import APIRouter

from api.api import Columns
from classes import ColumnInsert, ColumnUpdate

router = APIRouter()


@router.get('/getall', description='Получаем столбцы доски')
async def get_all():
    column = Columns()
    res = await column.column_read_all()
    return res

@router.get('/get', description='Получаем конкретный столбец')
async def get_card(column_id: int):
    column = Columns()
    res = column.column_read(column_id)
    return res


@router.post('/create', description='Создаём столбец доски')
async def create_column(insertion: ColumnInsert):
    column = Columns()
    step = await column.column_create(insertion)
    res = await column.show_created(step)
    return res

@router.post('/upd', description='Изменяем столбец')
async def update_column(column_id: int, insertion: ColumnUpdate):
    column = Columns()
    await column.column_update(column_id, insertion)
    res = await column.show_created(column_id)
    return res

@router.post('/del', description='Удаляем столбец')
async def delete_column(column_id: int):
    column = Columns()
    res = await column.show_deleted(column_id)
    await column.column_delete(column_id)
    return res