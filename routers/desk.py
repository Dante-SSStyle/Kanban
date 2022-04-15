from typing import List

from api.api import Desk, DeskInsert, JoinModule
from fastapi import APIRouter

router = APIRouter()


@router.get('/desks', description='Получаем все доски')
async def get_all():
    desk = Desk()
    res = await desk.desk_read_all()
    return res

@router.get('/get', description='Получаем доску')
async def get_desk(desk_id: int):
    desk = Desk()
    res = await desk.desk_read(desk_id)
    return res

@router.post('/create', description='Создаём доску')
async def create_desk(insertion: DeskInsert):
    desk = Desk()
    step = await desk.desk_create(insertion)
    res = await desk.show_created_desk(step)
    return res
