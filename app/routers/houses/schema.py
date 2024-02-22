from pydantic import BaseModel
from app.routers.houses.models import HousingTypes

class HousesSchema(BaseModel):
    housing_type: HousingTypes
    url: str
    adress: str
    price: int
    size: int
    with_furniture: bool