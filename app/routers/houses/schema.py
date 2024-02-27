from pydantic import BaseModel, Json
from app.routers.houses.models import HousingTypes

class HousesSchema(BaseModel):
    housing_type: HousingTypes 
    url: str
    adress: str | None
    price: str | None
    short_info: Json | None
    land_info: str | None
    created_statement: str
    updated_statement: str | None


class ReadHouseSchema(BaseModel):
    id: int
    housing_type: HousingTypes 
    url: str
    adress: str | None
    price: str | None
    short_info: Json | None
    land_info: str | None
    created_statement: str
    updated_statement: str | None


class ReadHousesSchema(BaseModel):
    data: list[ReadHouseSchema]