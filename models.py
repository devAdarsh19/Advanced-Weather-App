import datetime

from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, Float, DateTime, Date, func
from sqlalchemy.orm import relationship
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
    
    forecasts = relationship("ForecastDay", back_populates="weather", cascade="all, delete-orphan")
    
class ForecastDay(Base):
    __tablename__ = "forecast_day"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    maxtemp_c = Column(Float)
    mintemp_c = Column(Float)
    maxtemp_f = Column(Float)
    mintemp_f = Column(Float)
    avgtemp_c = Column(Float)
    avgtemp_f = Column(Float)
    condition = Column(String)
    
    weather_id = Column(Integer, ForeignKey("weather.id"))
    weather = relationship("Weather", back_populates="forecasts")
    
    hours = relationship("ForecastHour", back_populates="forecast_day", cascade="all, delete-orphan")

class ForecastHour(Base):
    __tablename__ = "forecast_hour"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime)
    temp_c = Column(Float)
    temp_f = Column(Float)
    condition = Column(String)
    
    forecast_day_id = Column(Integer, ForeignKey("forecast_day.id"))
    forecast_day = relationship("ForecastDay", back_populates="hours")
    
    
