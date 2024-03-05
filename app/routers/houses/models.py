import enum
from app.helpers.database import BaseDBModel
from sqlalchemy.dialects.postgresql import ENUM as SQLAlchemyEnum
from sqlalchemy import Column, Integer, String, JSON


class HousingTypes(str, enum.Enum):
    house = "house"
    apartment = "apartment"


class Houses(BaseDBModel):
    __tablename__ = "Houses"

    id = Column(Integer, primary_key=True, autoincrement=True)

    housing_type = Column(SQLAlchemyEnum(HousingTypes), default=None)
    url = Column(String)
    address = Column(String)
    price = Column(String)
    short_info = Column(JSON)
    land_info = Column(String)
    created_statement = Column(String)
    updated_statement = Column(String)
