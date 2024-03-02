from pydantic import BaseModel, Field, Json
from app.routers.houses.models import HousingTypes

class GetHouseSchema(BaseModel):
    id: int
    housing_type: HousingTypes = Field(title="Type")
    url: str
    adress: str | None
    price: str | None
    created_statement: str = Field(title="Created")
    updated_statement: str | None = Field(title="Updated")


class GetHousesSchema(BaseModel):
    data: list[GetHouseSchema]

class GetInfoSchema(BaseModel):
    id: int
    housing_type: HousingTypes = Field(title="Type")
    url: str
    adress: str | None
    price: str | None
    land_info: str | None
    short_info: Json | None
    created_statement: str = Field(title="Created")
    updated_statement: str | None = Field(title="Updated")


class GetHouseInfoSchema(BaseModel):
    data: list[GetInfoSchema]

