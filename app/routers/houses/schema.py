from pydantic import BaseModel
from app.routers.houses.models import HousingTypes

class HousesSchema(BaseModel):
    housing_type: HousingTypes
    url: str
    adress: str
    price: str
    condition: str
    building_type: str
    area: str
    rooms_count: str