from fastapi import APIRouter, Query
from classes import Card
from models import CardCreate, CardExtract, CardExtractAll, CardUpdate, CardDelete, CardOrder

router = APIRouter()


@router.get('/', description='Получаем карточки')
async def get_all_cards(desk_id: int = Query(...), column_id: int = Query(...)):
    return Card.extract_all(CardExtractAll(desk_id=desk_id, column_id=column_id))


@router.get('/{card_id}', description='Получаем конкретную карточку')
async def get_card(card_id: int):
    return Card.extract(CardExtract(id=card_id))


@router.post('/', description='Создаём карточку')
async def create_card(card: CardCreate):
    return Card.create(card)


@router.put('/', description='Изменяем карточку')
async def update_card(card: CardUpdate):
    return Card.update(card)


@router.put('/order', description='Меняем порядок карточек')
async def upd_order_column(card: CardOrder):
    return Card.upd_order(card)


@router.delete('/', description='Удаляем карточку')
async def delete_card(card: CardDelete):
    return Card.delete(card)
