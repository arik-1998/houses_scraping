from sqlalchemy.orm import Session
from sqlalchemy import select
from app.routers.houses.schema import HousesSchema
from app.routers.houses.models import Houses
from sqlalchemy.ext.asyncio import AsyncSession


class HousesCRUD():

    @classmethod
    async def add_house(cls, data:HousesSchema, db: AsyncSession):
        house = Houses(**data)
        db.add(house)


    @classmethod
    async def read_houses(cls, db: Session):
        query = select(Houses)
        result = await db.execute(query)
        return result.scalars().all()
    

    @classmethod
    def add_house_syncron(cls, data:HousesSchema, db: AsyncSession):
        house = Houses(**data)
        db.add(house)
        