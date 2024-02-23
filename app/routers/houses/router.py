from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.helpers.database import get_db
from app.routers.houses.async_scraper import async_scraper
from app.routers.houses.scraper import get_page_info

router = APIRouter()


@router.post("/async_scrap_data")
async def async_scrap_data(db: Session = Depends(get_db)):
    await async_scraper(db)
    return {"code": status.HTTP_200_OK}


@router.post("/scrap_data")
async def scrap_data(db: Session = Depends(get_db)):
    get_page_info(db)
    return {"code": status.HTTP_200_OK}