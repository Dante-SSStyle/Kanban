from fastapi import FastAPI

from api.api import database
from routers import desk_router, card_router, column_router

import databases
from sqlalchemy import Column
import sqlalchemy

# DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/Test'
# database = databases.Database(DATABASE_URL)
#
# metadata = sqlalchemy.MetaData()
# DeskSQL = sqlalchemy.Table(
#     'desk',
#     metadata,
#     Column('desk_id', sqlalchemy.Integer, primary_key=True),
#     Column('title', sqlalchemy.String),
#     Column('create_date', sqlalchemy.Date),
#     Column('update_date', sqlalchemy.Date),
# )
#
# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.create_all(engine)

app = FastAPI(
    title='Kanban',
    description='Моя канбан-доска',
    docs_url='/docs',
    redoc_url='/doc'
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


@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
