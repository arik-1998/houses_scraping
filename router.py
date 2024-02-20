from typing import Annotated
from fastapi import APIRouter, Depends, status
from schema import HousesSchema
from crud import HousesCRUD

router = APIRouter()

@router.post("/add_house")
async def add_house(house:Annotated[HousesSchema, Depends()]):
    await HousesCRUD.add_house(house)
    return {"code": status.HTTP_200_OK}
