from sqlalchemy import Column, Integer, String
from .database import Base


class CityDistance(Base):

    __tablename__ = "city_distances"

    id = Column(Integer, primary_key=True)

    city1 = Column(String, index=True)

    city2 = Column(String, index=True)

    distance = Column(Integer)
