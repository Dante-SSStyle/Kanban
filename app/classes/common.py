from pydantic import ValidationError

from exceptions import KanbanException


class CommonClass:

    @classmethod
    def _check(cls, query):
        try:
            query
        except TypeError or ValueError:
            raise KanbanException(400, 'Неверный ввод данных!')
        except Exception:
            raise KanbanException(418, 'Упс!')
        except ValidationError:
            raise KanbanException(400, 'Неверный ввод данных!')
        return query

    @classmethod
    def _check404(cls, query):
        if not query:
            raise KanbanException(404, 'Ничего не найдено!')
        return query
