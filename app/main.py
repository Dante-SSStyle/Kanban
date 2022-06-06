from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routers import desk_router, card_router, column_router, page_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from db import database_channel


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
    page_router,
    tags=['page'],
    dependencies=[]
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
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return templates.TemplateResponse("error.html",
                                      {"request": request, "detail": 'Неверный ввод данных!', "status_code": 422})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("error.html",
                                      {"request": request, "detail": str(exc.detail), "status_code": exc.status_code},
                                      exc.status_code)


@app.on_event('startup')
async def startup():
    await database_channel.connect()


@app.on_event('shutdown')
async def shutdown():
    await database_channel.disconnect()
