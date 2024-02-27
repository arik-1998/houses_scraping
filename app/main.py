from fastapi import FastAPI
from fastapi import status
from .routers.houses.router import router

app = FastAPI()
app.include_router(router)
