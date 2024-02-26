from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.helpers.database import get_db
from app.routers.houses.async_scraper import async_scraper
from app.routers.houses.scraper import get_page_info
from app.routers.houses.crud import HousesCRUD
from app.routers.houses.schema import ReadHousesSchema
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/async_scrap_data")
async def async_scrap_data(db: AsyncSession = Depends(get_db)):
    await async_scraper(db)
    return {"code": status.HTTP_200_OK}


@router.post("/scrap_data")
async def scrap_data(db: Session = Depends(get_db)):
    get_page_info(db)
    return {"code": status.HTTP_200_OK}


@router.get("/get_house_example")
async def get_house_example(db: Session = Depends(get_db)):
    data = await HousesCRUD.read_houses(db)
    houses = ReadHousesSchema(**jsonable_encoder(data))
    return {"data": houses, "code": status.HTTP_200_OK}
