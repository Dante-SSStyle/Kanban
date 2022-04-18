from fastapi.exceptions import HTTPException


class KanbanException(HTTPException):
    pass