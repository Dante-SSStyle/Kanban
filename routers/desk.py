from typing import List
from fastapi import APIRouter
from classes import Desk
from models import DeskInsert, DeskBase, DeskFull

router = APIRouter()


@router.get('/getall', response_model=List[DeskBase], description='Получаем все доски')
async def get_all():
    desk = Desk()
    res = await desk.desk_read_all()
    return res


@router.get('/get', response_model=List[DeskFull], description='Получаем доску')
async def get_desk(desk_id: int):
    desk = Desk()
    res = desk.desk_read(desk_id)
    return res


@router.post('/create', response_model=List[DeskBase], description='Создаём доску')
async def create_desk(insertion: DeskInsert):
    desk = Desk()
    step = await desk.desk_create(insertion)
    res = await desk.show_created(step)
    return res


@router.delete('/del', response_model=List[DeskBase], description='Удаляем доску')
async def delete_desk(desk_id: int):
    desk = Desk()
    res = await desk.fetch_line(desk_id)
    await desk.desk_delete(desk_id)
    return res


@router.put('/upd', response_model=List[DeskBase], description='Изменяем доску')
async def update_desk(desk_id: int, insertion: DeskInsert):
    desk = Desk()
    await desk.desk_update(desk_id, insertion)
    res = await desk.show_created(desk_id)
    return res
