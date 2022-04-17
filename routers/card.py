from api.api import Card
from fastapi import APIRouter

from classes import CardInsert, CardUpdate

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
    res = await card.show_created(step)
    return res

@router.post('/upd', description='Изменяем карточку')
async def update_card(card_id: int, insertion: CardUpdate):
    card = Card()
    await card.card_update(card_id, insertion)
    res = await card.show_created(card_id)
    return res

@router.post('/del', description='Удаляем карточку')
async def delete_column(card_id: int):
    card = Card()
    res = await card.show_deleted(card_id)
    await card.card_delete(card_id)
    return res
