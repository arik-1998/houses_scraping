from pydantic import BaseModel
from models import HousingTypes

class HousesSchema(BaseModel):
    housing_type: HousingTypes
    url: str
    adress: str
    price: int
    size: int
    with_furniture: bool