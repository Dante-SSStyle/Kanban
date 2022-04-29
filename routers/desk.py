from typing import List
from fastapi import APIRouter, Request
from classes import Desk
from models import DeskInsert, DeskBase, DeskFull
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/getall', response_model=List[DeskFull], description='Получаем все доски')
async def get_all(request: Request):
    desk = Desk()
    res = await desk.desk_read_all()
    return templates.TemplateResponse("desks.html", {"request": request, "res": res})


@router.get('/get', response_model=List[DeskFull], description='Получаем доску')
async def get_desk(request: Request, desk_id: int):
    desk = Desk()
    res = desk.desk_read(desk_id)
    return res


@router.post('/create', response_model=List[DeskBase], description='Создаём доску')
async def create_desk(insertion: DeskInsert):
    desk = Desk()
    await desk.desk_create(insertion)
    res = await desk.show_created(insertion)
    return res


@router.put('/upd', response_model=List[DeskBase], description='Изменяем доску')
async def update_desk(desk_id: int, insertion: DeskInsert):
    desk = Desk()
    await desk.desk_update(desk_id, insertion)
    res = await desk.show_created(insertion, desk_id)
    return res


@router.delete('/del', response_model=List[DeskBase], description='Удаляем доску')
async def delete_desk(desk_id: int):
    desk = Desk()
    res = await desk.fetch_line(desk_id)
    await desk.desk_delete(desk_id)
    return res
