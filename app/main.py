from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
# from db_old import database
from routers import desk_router, card_router, column_router
from fastapi import APIRouter, Request, Query
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse
from config import HOST

from sqlalchemy.orm import Session
from db import database_channel
from classes import Desk
from models import DeskCreate, DeskExtract, DeskExtractAll, DeskDelete



app = FastAPI(
    title='Kanban',
    description='Моя канбан-доска',
    docs_url='/docs',
    redoc_url='/doc'
)

# Добавление поддержки политик CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["*"]
)




app.include_router(
    desk_router,
    prefix='/desks',
    tags=['desk'],
    dependencies=[]
)
app.include_router(
    card_router,
    prefix='/cards',
    tags=['card'],
    dependencies=[]
)
app.include_router(
    column_router,
    prefix='/columns',
    tags=['column'],
    dependencies=[]
)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")


# Перехват ошибок
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("error.html", {"request": request, "detail": str(exc.detail), "status_code": exc.status_code})

@app.get("/tmp")
def ttt():
    return "ready!"

@app.get("/dsk")
def tt1():
    return Desk.extract_all()

@app.get("/dsk/{dsk_id}")
def tt1(dsk_id: int):
    return Desk.extract(DeskExtract(id=dsk_id))

@app.post("/dsk")
def tt2(desk: DeskCreate):
    return Desk.create(desk)

@app.delete("/dsk")
def tt3(desk: DeskDelete):
    return Desk.delete(desk)

@app.get("/")
def test():
    return RedirectResponse(f"{HOST}/desks/all")


@app.on_event('startup')
async def startup():
    await database_channel.connect()


@app.on_event('shutdown')
async def shutdown():
    await database_channel.disconnect()
