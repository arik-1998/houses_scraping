from sqlalchemy.orm import Session
from app.routers.houses.schema import HousesSchema
from app.routers.houses.models import Houses

async def insert_data(db: Session, instance):
    db.add(instance)
    await db.commit()
    db.refresh(instance)
    return instance

class HousesCRUD():

    @classmethod
    async def add_house(cls, data:HousesSchema, db: Session):
        house = Houses(**data)
        await insert_data(db, house)


    @classmethod
    async def read_houses(cls, db: Session):
        return await db.query(Houses).first()
        