from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.helpers.database import get_db
from app.routers.houses.schema import HousesSchema
from app.routers.houses.crud import HousesCRUD
from app.routers.houses.scrap import get_page_info

router = APIRouter()

@router.post("/add_house")
async def add_house(house:Annotated[HousesSchema, Depends()], db: Session = Depends(get_db)):
    HousesCRUD.add_house(house, db)
    return {"code": status.HTTP_200_OK}


@router.post("/scrap_data")
async def scrap_data(db: Session = Depends(get_db)):
    get_page_info(db)
    return {"code": status.HTTP_200_OK}