from fastapi import APIRouter
from classes import Desk
from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete

router = APIRouter()


@router.get('/', description='Получаем все доски')
def get_all_desks():
    desks_list = Desk.extract_all()
    return desks_list


@router.get('/{desk_id}', description='Получаем доску')
def get_desk(desk_id: int):
    desk_info = Desk.extract(DeskExtract(id=desk_id))
    return desk_info


@router.post('/', description='Создаём доску')
def create_desk(desk: DeskCreate):
    return Desk.create(desk)


@router.put('/', description='Изменяем доску')
def update_desk(desk: DeskUpdate):
    return Desk.update(desk)


@router.delete('/', description='Удаляем доску')
def delete_desk(desk: DeskDelete):
    return Desk.delete(desk)
