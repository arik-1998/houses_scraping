from pydantic import BaseModel, Json
from app.routers.houses.models import HousingTypes

class HousesSchema(BaseModel):
    housing_type: HousingTypes | None
    url: str | None
    adress: str | None
    price: str | None
    short_info: Json | None


class ReadHousesSchema(HousesSchema):
    id: int | None
    housing_type: HousingTypes | None
    url: str | None
    adress: str | None
    price: str | None
    short_info: Json | None