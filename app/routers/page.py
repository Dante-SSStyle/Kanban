from fastapi import APIRouter, Request
from classes import Desk
from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete
from fastapi.templating import Jinja2Templates
from config import HOST


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get('/', description='Получаем список досок')
def index(request: Request):
    desks_list = Desk.extract_all()
    return templates.TemplateResponse("index.html", {"request": request, "desks_list": desks_list, "host": HOST})


@router.get('/{desk_id}', description='Список карточек для выбранной доски')
def chosen_desk(request: Request, desk_id: int):
    desk_info = Desk.extract(DeskExtract(id=desk_id))
    # return desk_info
    return templates.TemplateResponse("desk.html", {"request": request, "host": HOST, **desk_info})
