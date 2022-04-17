from api.api import Desk
from fastapi import APIRouter

from classes import DeskInsert

router = APIRouter()


@router.get('/getall', description='Получаем все доски')
async def get_all():
    desk = Desk()
    res = await desk.desk_read_all()
    return res

@router.get('/get', description='Получаем доску')
async def get_desk(desk_id: int):
    desk = Desk()
    res = desk.desk_read(desk_id)
    return res

@router.post('/create', description='Создаём доску')
async def create_desk(insertion: DeskInsert):
    desk = Desk()
    step = await desk.desk_create(insertion)
    res = await desk.show_created(step)
    return res

@router.post('/del', description='Удаляем доску')
async def delete_desk(desk_id: int):
    desk = Desk()
    res = await desk.show_deleted(desk_id)
    await desk.desk_delete(desk_id)
    return res

@router.post('/upd', description='Изменяем доску')
async def update_desk(desk_id: int, insertion: DeskInsert):
    desk = Desk()
    await desk.desk_update(desk_id, insertion)
    res = await desk.show_created(desk_id)
    return res
