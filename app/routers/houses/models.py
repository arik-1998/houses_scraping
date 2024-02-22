import enum
from app.helpers.database import BaseDBModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM as SQLAlchemyEnum
from sqlalchemy import Column, Integer, String, Boolean


class HousingTypes(str, enum.Enum):
    house = "house"
    apartment = "apartment"

class Houses(BaseDBModel):
    __tablename__ = "Houses"

    id = Column(Integer, primary_key=True, autoincrement=True)

    housing_type = Column(SQLAlchemyEnum(HousingTypes), default=None)
    url = Column(String)
    adress = Column(String)
    price = Column(Integer)
    size = Column(Integer)
    with_furniture = Column(Boolean, default=False)