from fastapi import FastAPI
from db import database
from routers import desk_router, card_router, column_router
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"detail": str(exc.detail)}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({"detail": str("lox")}, status_code=400)

@app.get("/")
def test():
    return RedirectResponse("http://127.0.0.1:8000/desks/getall")


@app.get("/test")
def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


@app.get("/test2")
def test2():
    return {"test": "lox"}


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
