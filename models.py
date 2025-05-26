import datetime

from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, Float, DateTime, func
from database import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    location_name = Column(String, index=True)
    region = Column(String)
    country = Column(String)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    timezone = Column(String)
    localtime = Column(DateTime)
    temp_c = Column(Float)
    temp_f = Column(Float)
    condition = Column(String)
    fetched_at = Column(DateTime, default=func.now())
