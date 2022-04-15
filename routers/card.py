from api.api import Card, CardInsert
from fastapi import APIRouter

router = APIRouter()


@router.get('/getall', description='Получаем карты')
async def get_all():
    card = Card()
    res = await card.card_read_all()
    return res


@router.get('/get', description='Получаем конкретную карту')
async def get_card(card_id: int):
    card = Card()
    res = await card.card_read(card_id)
    return res


@router.post('/create', description='Создаём карточку')
async def create_card(insertion: CardInsert):
    card = Card()
    step = await card.card_create(insertion)
    res = await card.show_created_card(step)
    return res

