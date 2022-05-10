from typing import List
from fastapi import APIRouter
from classes import CardOld as Card
from models import CardInsert, CardUpdate, CardBase

router = APIRouter()


@router.get('/all', response_model=List[CardBase], description='Получаем карты')
async def get_all_cards():
    card = Card()
    res = await card.card_read_all()
    return res


@router.get('/', response_model=List[CardBase], description='Получаем конкретную карту')
async def get_card(card_id: int):
    card = Card()
    res = await card.card_read(card_id)
    return res


@router.post('/', response_model=List[CardBase], description='Создаём карточку')
async def create_card(insertion: CardInsert):
    card = Card()
    await card.card_create(insertion)
    res = await card.show_created(insertion)
    return res


@router.put('/', response_model=List[CardBase], description='Изменяем карточку')
async def update_card(card_id: int, insertion: CardUpdate):
    card = Card()
    await card.card_update(card_id, insertion)
    res = await card.show_created(insertion, card_id)
    return res


@router.delete('/', response_model=List[CardBase], description='Удаляем карточку')
async def delete_column(card_id: int):
    card = Card()
    res = await card.fetch_line(card_id)
    await card.card_delete(card_id)
    return res
