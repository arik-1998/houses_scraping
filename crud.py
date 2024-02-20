from database import new_session
from schema import HousesSchema
from models import Houses

class HousesCRUD():
    @classmethod
    async def add_house(cls, data:HousesSchema):
        async with new_session() as session:
            house_dict = data.model_dump()
            house = Houses(**house_dict)
            session.add(house)
            await session.commit()