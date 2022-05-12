from typing import List
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from classes import Desk
from config import HOST
from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/all', description='Получаем все доски')
def get_all_cards(request: Request):
    desks_list = Desk.extract_all()
    return templates.TemplateResponse("index.html", {"request": request, "desks_list": desks_list, "host": HOST})


@router.get('/{desk_id}', description='Получаем доску')
def get_desk(request: Request, desk_id: int):
    desk_info = Desk.extract(DeskExtract(id=desk_id))
    # return desk_info
    return templates.TemplateResponse("normal_desk.html", {"request": request, "desk_info": desk_info, "host": HOST})


@router.post('/', description='Создаём доску')
def create_desk(desk: DeskCreate):
    return Desk.create(desk)


@router.put('/', description='Изменяем доску')
def update_desk(desk: DeskUpdate):
    return Desk.update(desk)


@router.delete('/', description='Удаляем доску')
def delete_desk(desk: DeskDelete):
    return Desk.delete(desk)
