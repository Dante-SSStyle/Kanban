from typing import List
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from classes import Desk
from models import DeskInsert, DeskBase, DeskFull
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# todo response model должен быть html или не быть вообще
@router.get('/all', response_model=List[DeskFull], description='Получаем все доски')
async def get_all_cards(request: Request):
    dsk = Desk()
    desks_list = await dsk.desk_read_all()
    return templates.TemplateResponse("desks.html", {"request": request, "desks_list": desks_list})


@router.get('/', response_model=List[DeskFull], description='Получаем доску')
async def get_desk(request: Request, desk_id: int):
    dsk = Desk()
    desk_info = dsk.desk_read(desk_id)[0]

    # todo здесь получаем колонки, карточки, которые будем вставлять в jinja

    return templates.TemplateResponse("desk.html", {"request": request, "desk_info": desk_info})


@router.post('/', response_model=List[DeskBase], description='Создаём доску')
async def create_desk(insertion: DeskInsert):
    dsk = Desk()
    await dsk.desk_create(insertion)
    res = await dsk.show_created(insertion)
    return res


@router.put('/', response_model=List[DeskBase], description='Изменяем доску')
async def update_desk(desk_id: int, insertion: DeskInsert):
    dsk = Desk()
    await dsk.desk_update(desk_id, insertion)
    res = await dsk.show_created(insertion, desk_id)
    return res


@router.delete('/', response_model=List[DeskBase], description='Удаляем доску')
async def delete_desk(desk_id: int):
    dsk = Desk()
    res = await dsk.fetch_line(desk_id)
    await dsk.desk_delete(desk_id)
    return res
