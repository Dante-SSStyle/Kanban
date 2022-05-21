from typing import Optional
from sqlalchemy import func
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
# from db import sosi as session, ColumnSQL, DeskSQL, CardSQL, debil as database
from exceptions import KanbanException


class MainInnerClass:
    def __init__(self):
        pass

    def _content_check(self, table, clause: Optional = True):
        if not session.query(table).filter(clause).all():
            raise KanbanException(404, 'Не найдено ни одного элемента')

    '''Проверка данных перед использованием JOIN для вывода полной информации о столбцах/доске'''
    def _column_check_res(self, res, column_id):
        self._content_check(ColumnSQL, ColumnSQL.c.column_id == column_id)
        if not res:
            return session.query(ColumnSQL).filter(ColumnSQL.c.column_id == column_id).all()
        return res

    def _desk_check_res(self, res, desk_id):
        self._content_check(DeskSQL, DeskSQL.c.desk_id == desk_id)
        if not session.query(DeskSQL, ColumnSQL).join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id2)\
                .filter(DeskSQL.c.desk_id == desk_id).all():
            return session.query(DeskSQL).filter(DeskSQL.c.desk_id == desk_id).all()
        if not res:
            return session.query(DeskSQL, ColumnSQL).join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id2)\
                .filter(DeskSQL.c.desk_id == desk_id).all()
        return res
    '''Проверка и установка позиции столбца/карточки'''
    def _column_check_order(self, get_order):
        if get_order[0][0] is None:
            order = 0
            return order
        order = get_order[0][0]
        return order

    def _card_check_order(self, get_order):
        if get_order[0][0] is None:
            order = 0
            return order
        order = get_order[0][0]
        return order

    async def _exception_catcher(self, query):
        res = database.execute(query)
        try:
            await res
        except ForeignKeyViolationError:
            raise KanbanException(404, 'Доски/таблицы с таким id не существует')
        except UniqueViolationError:
            raise KanbanException(400, 'Такое имя уже используется')
        except Exception:
            raise KanbanException(418, 'Упс, что-то сломалось!')
        return res

    def _createform(self, data):
        response = []
        cards = []
        columns = []
        form = {
            'desk_id': int,
            'desk_title': str,
            'column_id': None,
            'column_title': None,
            'column_order_num': None,
            'cards': cards
        }
        card_form = {
            "card_id": int,
            "card_title": str,
            "content": str,
            "card_create_date": data,
            "card_update_date": data,
            "end_date": data,
            "card_order_num": int
        }

        for dictnr in data:
            # print(response, '\n')
            form.update({
                'desk_id': dictnr.desk_id,
                'desk_title': dictnr.desk_title
            })
            if 'column_id' in dictnr.keys():
                if dictnr.column_id not in columns:
                    cards = []
                    if form['column_id']:
                        response.append(form.copy())
                    form.update({'cards': cards})
                    columns.append(dictnr.column_id)
                    form.update({
                        'column_id': dictnr.column_id,
                        'column_title': dictnr.column_title,
                        'column_order_num': dictnr.column_order_num
                    })
                    if 'card_id' in dictnr.keys():
                        if dictnr.card_id:
                            card_form.update({
                                "card_id": dictnr.card_id,
                                "card_title": dictnr.card_title,
                                "content": dictnr.content,
                                "card_create_date": dictnr.card_create_date,
                                "card_update_date": dictnr.card_update_date,
                                "end_date": dictnr.end_date,
                                "card_order_num": dictnr.card_order_num
                            })
                            cards.append(card_form.copy())
                            form.update({'cards': cards})
                else:
                    card_form.update({
                        "card_id": dictnr.card_id,
                        "card_title": dictnr.card_title,
                        "content": dictnr.content,
                        "card_create_date": dictnr.card_create_date,
                        "card_update_date": dictnr.card_update_date,
                        "end_date": dictnr.end_date,
                        "card_order_num": dictnr.card_order_num
                    })
                    cards.append(card_form.copy())
                    form.update({'cards': cards})

        else:
            response.append(form.copy())
            # print(response,'\n')
        return response

class Desk(MainInnerClass):
    def __init__(self):
        super().__init__()
        self.desks_select = DeskSQL.select()

    def desk_read_all(self):
        # self._content_check(DeskSQL)
        res = database.fetch_all(self.desks_select.order_by(DeskSQL.c.desk_id))
        return res

    def desk_read(self, desk_id: int):
        res = session.query(DeskSQL, ColumnSQL, CardSQL)\
            .join(ColumnSQL, DeskSQL.c.desk_id == ColumnSQL.c.desk_id2)\
            .join(CardSQL, ColumnSQL.c.column_id == CardSQL.c.column_id2, isouter=True)\
            .filter(DeskSQL.c.desk_id == desk_id).order_by(ColumnSQL.c.column_order_num).all()
        check = self._desk_check_res(res, desk_id)
        result = self._createform(check)
        return result

    def desk_create(self, insertion):
        query = DeskSQL.insert().values(
            desk_title=insertion.title
        )
        res = self._exception_catcher(query)
        return res

    def show_created(self, insertion, desk_id: Optional = None):
        if desk_id:
            new_record = self.desks_select.where(DeskSQL.c.desk_id == desk_id)
        else:
            get_id = session.query(DeskSQL).filter(DeskSQL.c.desk_title == insertion.title).all()
            new_record = self.desks_select.where(DeskSQL.c.desk_id == get_id[0][0])
        res = database.fetch_all(new_record)
        return res

    def desk_update(self, desk_id: int, insertion):
        self._content_check(DeskSQL, DeskSQL.c.desk_id == desk_id)
        query = DeskSQL.update().where(DeskSQL.c.desk_id == desk_id).values(
            desk_title=insertion.title
        )
        res = self._exception_catcher(query)
        return res

    def desk_delete(self, desk_id: int):
        self._content_check(DeskSQL, DeskSQL.c.desk_id == desk_id)
        query = DeskSQL.delete().where(DeskSQL.c.desk_id == desk_id)
        res = database.execute(query)
        return res

    def fetch_line(self, desk_id: int):
        deleted_record = self.desks_select.where(DeskSQL.c.desk_id == desk_id)
        res = database.fetch_all(deleted_record)
        return res


class Columns(MainInnerClass):
    def __init__(self):
        super().__init__()
        self.columns_select = ColumnSQL.select()

    def column_read_all(self):
        self._content_check(ColumnSQL)
        res = database.fetch_all(self.columns_select)
        return res

    def column_read(self, column_id: int):
        res = session.query(ColumnSQL, CardSQL).join(CardSQL, ColumnSQL.c.column_id == CardSQL.c.column_id2)\
            .filter(ColumnSQL.c.column_id == column_id).all()
        result = self._column_check_res(res, column_id)
        return result

    def column_create(self, insertion):
        get_order = session.query(func.max(ColumnSQL.c.column_order_num))\
            .filter(ColumnSQL.c.desk_id2 == insertion.desk_id2).all()
        order = self._column_check_order(get_order)
        query = ColumnSQL.insert().values(
            column_title=insertion.title,
            column_order_num=order+1,
            desk_id2=insertion.desk_id2
        )
        res = self._exception_catcher(query)
        return res

    def show_created(self, insertion, column_id: Optional = None):
        if column_id:
            new_record = self.columns_select.where(ColumnSQL.c.column_id == column_id)
        else:
            get_id = session.query(ColumnSQL).filter(ColumnSQL.c.column_title == insertion.title).all()
            new_record = self.columns_select.where(ColumnSQL.c.column_id == get_id[0][0])
        res = database.fetch_all(new_record)
        return res

    def column_update(self, column_id: int, insertion):
        self._content_check(ColumnSQL, ColumnSQL.c.column_id == column_id)
        query = ColumnSQL.update().where(ColumnSQL.c.column_id == column_id).values(
            column_title=insertion.title,
            column_order_num=insertion.order_num
        )
        res = self._exception_catcher(query)
        return res

    def column_delete(self, column_id: int):
        self._content_check(ColumnSQL, ColumnSQL.c.column_id == column_id)
        query = ColumnSQL.delete().where(ColumnSQL.c.column_id == column_id)
        res = database.execute(query)
        return res

    def fetch_line(self, column_id: int):
        deleted_record = self.columns_select.where(ColumnSQL.c.column_id == column_id)
        res = database.fetch_all(deleted_record)
        return res


class Card(MainInnerClass):
    def __init__(self):
        super().__init__()
        self.cards_select = CardSQL.select()

    def card_read_all(self):
        self._content_check(CardSQL)
        res = database.fetch_all(self.cards_select)
        return res

    def card_read(self, card_id: int):
        self._content_check(CardSQL, CardSQL.c.card_id == card_id)
        select = self.cards_select.where(CardSQL.c.card_id == card_id)
        res = database.fetch_all(select)
        return res

    def card_create(self, insertion):
        get_order = session.query(func.max(CardSQL.c.card_order_num))\
            .filter(CardSQL.c.column_id2 == insertion.column_id2, CardSQL.c.desk_id3 == insertion.desk_id3).all()
        order = self._card_check_order(get_order)
        query = CardSQL.insert().values(
            card_title=insertion.title,
            content=insertion.content,
            end_date=insertion.end_date,
            card_order_num=order+1,
            column_id2=insertion.column_id2,
            desk_id3=insertion.desk_id3
        )
        res = self._exception_catcher(query)
        return res

    def show_created(self, insertion, card_id: Optional = None):
        if card_id:
            new_record = self.cards_select.where(CardSQL.c.card_id == card_id)
        else:
            get_id = session.query(CardSQL).filter(CardSQL.c.card_title == insertion.title).all()
            new_record = self.cards_select.where(CardSQL.c.card_id == get_id[0][0])
        res = database.fetch_all(new_record)
        return res

    def card_update(self, card_id: int, insertion):
        self._content_check(CardSQL, CardSQL.c.card_id == card_id)
        query = CardSQL.update().where(CardSQL.c.card_id == card_id).values(
            card_title=insertion.title,
            content=insertion.content,
            end_date=insertion.end_date,
            card_order_num=insertion.order_num,
            column_id2=insertion.column_id2,
        )
        res = self._exception_catcher(query)
        return res

    def card_delete(self, card_id: int):
        self._content_check(CardSQL, CardSQL.c.card_id == card_id)
        query = CardSQL.delete().where(CardSQL.c.card_id == card_id)
        res = database.execute(query)
        return res

    def fetch_line(self, card_id: int):
        fetched_record = self.cards_select.where(CardSQL.c.card_id == card_id)
        res = database.fetch_all(fetched_record)
        return res
