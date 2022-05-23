from fastapi import APIRouter
from classes import Desk, Column
from models import DeskCreate, DeskExtract, DeskUpdate, DeskDelete, ColumnCreate

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
    new_desk_info = Desk.create(desk)
    ColumnCreate.desk_id = new_desk_info.id
    clmns = ['Backlog', 'ToDo', 'Doing', 'Done!']
    for i in clmns:
        ColumnCreate.title = i
        Column.create(ColumnCreate)
    return new_desk_info


@router.put('/', description='Изменяем доску')
def update_desk(desk: DeskUpdate):
    return Desk.update(desk)


@router.delete('/', description='Удаляем доску')
def delete_desk(desk: DeskDelete):
    return Desk.delete(desk)
