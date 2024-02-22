from fastapi import FastAPI
from fastapi import status
from .routers.houses.router import router
from app.helpers.database import create_database

app = FastAPI()
app.include_router(router)

@app.post('/create_database')
async def route_create_database():
    create_database()
    return {"code": status.HTTP_200_OK}

