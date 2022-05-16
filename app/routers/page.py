from fastapi import APIRouter, Request
from classes import Desk, Card
from models import DeskExtract, CardExtract
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
    desk_info = Desk.extract(DeskExtract(id=desk_id), only_desk=False)
    return templates.TemplateResponse("desk.html", {"request": request, "host": HOST, **desk_info})


@router.get('/card/{card_id}', description='Выбранная карточка')
def chosen_card(request: Request, card_id: int):
    card_info = Card.extract(CardExtract(id=card_id), only_card=False)
    return templates.TemplateResponse("card.html", {"request": request, "host": HOST, **card_info})
