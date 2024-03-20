from fastapi import FastAPI
from app.routers.houses import router
from app.routers.admin import admin

app = FastAPI()
app.include_router(router.router)
app.include_router(admin.router)
