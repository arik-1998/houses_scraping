from sqlalchemy.orm import Session
from app.routers.houses.schema import HousesSchema
from app.routers.houses.models import Houses

def insert_data(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

class HousesCRUD():
    @classmethod
    def add_house(cls, data:HousesSchema, db):
        house_dict = data.model_dump()
        house = Houses(**house_dict)
        insert_data(db, house)