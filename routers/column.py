from fastapi import APIRouter

from api.api import ColumnInsert, Columns

router = APIRouter()


@router.get('/getall', description='Получаем столбцы доски')
async def get_all():
    column = Columns()
    res = await column.column_read_all()
    return res

@router.get('/get', description='Получаем конкретный столбец')
async def get_card(column_id: int):
    column = Columns()
    res = await column.column_read(column_id)
    return res


@router.post('/create', description='Создаём столбец доски')
async def create_column(insertion: ColumnInsert):
    column = Columns()
    step = await column.column_create(insertion)
    res = await column.show_created_column(step)
    return res
