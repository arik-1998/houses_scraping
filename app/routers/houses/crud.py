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
    def add_house(cls, data:HousesSchema, db: Session):
        house = Houses(**data)
        insert_data(db, house)


    @classmethod
    def read_houses(cls, db: Session):
        return db.query(Houses).first()
        