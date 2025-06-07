from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from pydantic import BaseModel
import redis
import json
from typing import Annotated, List
import requests
import os
import time
from datetime import datetime, timedelta

import models
import utils
from utils import logger
from database import engine, SessionLocal
from sqlalchemy.orm import Session, joinedload

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1"

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Initialize Redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



@app.get("/weather")
@limiter.limit("5/minute")
def get_weather(location_q: str, db: db_dependency, request: Request):
    @logger
    def get_weather():
        
        # Check for cached data in redis
        location_key = f"key:{location_q.strip().lower()}"
        
        cached = redis_client.get(location_key)
        if cached:
            print(f"Cache hit for location: {location_q}", flush=True)
            
            return json.loads(cached)
        
        ##############################################################################
        # Check DB to retrieve data if cache miss
        db_entry = (
            db.query(models.Weather)
            .filter(models.Weather.location_name.ilike(location_q))
            .order_by(models.Weather.localtime.desc())
            .first()
        )
        
        # if DB entry exists and is not stale, add to cache and return it
        if db_entry and db_entry.fetched_at > datetime.now() - timedelta(minutes=30):
            response = {
                "location_name": db_entry.location_name,
                "region": db_entry.region,
                "country": db_entry.country,
                "latitude": db_entry.latitude,
                "longitude": db_entry.longitude,
                "timezone": db_entry.timezone,
                "localtime": db_entry.localtime.isoformat(),
                "temp_c": db_entry.temp_c,
                "temp_f": db_entry.temp_f,
                "condition": db_entry.condition
            }
            redis_client.setex(location_key, 1800, json.dumps(response))
            
            return response
        
        #######################################################################
        # Hit the Free Weather API endpoint
        print(f"Hitting external API for location : {location_q}", flush=True)
        res = requests.get(url=f"{WEATHER_API_URL}/current.json?key={WEATHER_API_KEY}&q={location_q}")

        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch weather data")
        

        data = res.json()
        location = data["location"]
        current = data["current"]
        
        # If DB entry for location found
        if db_entry:
            print(f"Found an existing record")
            db_entry.localtime = location["localtime"]
            db_entry.temp_c = current["temp_c"]
            db_entry.temp_f = current["temp_f"]
            db_entry.condition = current["condition"]["text"]
            db_entry.fetched_at = datetime.now()
            
            db.commit()
            
            print(f"Updated existing weather DB record for location: {location_q}", flush=True)
        else:
            print(f"Creating new weather record for location : {location_q}", flush=True)
            current_weather = models.Weather(
                location_name=location["name"],
                region=location["region"],
                country=location["country"],
                latitude=location["lat"],
                longitude=location["lon"],
                timezone=location["tz_id"],
                localtime=location["localtime"],
                temp_c=current["temp_c"],
                temp_f=current["temp_f"],
                condition=current["condition"]["text"]
            )

            # Add to DB
            db.add(current_weather)
            db.commit()
            db.refresh(current_weather)
        
        # Add to cache
        redis_client.setex(location_key, 1800, json.dumps({
            "location_name":location["name"],
            "region":location["region"],
            "country":location["country"],
            "latitude":location["lat"],
            "longitude":location["lon"],
            "timezone":location["tz_id"],
            "localtime":location["localtime"],
            "temp_c":current["temp_c"],
            "temp_f":current["temp_f"],
            "condition":current["condition"]["text"]
        }))

        
        return data
    
    return get_weather()


@app.get("/forecast")
@limiter.limit("5/minute")
def get_forecast(location: str, days: int, db: db_dependency, request: Request):
    
    @logger
    def get_forecast():
        
        # Forecast limit is 5 days. Raise 400 error if days > 5
        if days > 5:
            raise HTTPException(status_code=400, detail="Forecast request cannot be more than 5 days")
        
        # We check for cache hit here
        
        location_forecast_key = f"forecast:{location.strip().lower()}:{days}"
        cached = redis_client.get(location_forecast_key)
        if cached:
            print(f"Cache hit for forecast location: {location}", flush=True)
            
            data = json.loads(cached)
            return data
        
        # Query database to check if location exists. Do not add again
        db_entry = (
            db.query(models.Weather)
            .filter(models.Weather.location_name.ilike(location.strip().lower()))
            .options(joinedload(models.Weather.forecasts).joinedload(models.ForecastDay.hours))
            .order_by(models.Weather.localtime.desc())
            .first()
        )
        
        # IF entry exists, let's check if it's stale
        # If stale, update the Weather table and then add the updated data to redis cache
        
        # If db_entry exists and is not stale
        if db_entry and db_entry.localtime > datetime.now() - timedelta(hours=1):
            
            response = utils.create_forecast_response(db_entry)
            redis_client.setex(location_forecast_key, time=3600, value=json.dumps(response))
            
            return response
        
        
        ################################################################################
        # Hitting the external API endpoint
        print(f"Hitting external endpoint for forecast location: {location}", flush=True)
        res = requests.get(url=f"{WEATHER_API_URL}/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}")

        if res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch forecast data")
        
        data = res.json()
        location_data = data["location"]
        current = data["current"]
        forecast = data["forecast"]["forecastday"]
        
        cache_weather_entry = None
        
        if db_entry:
            print(f"Updating an existing forecast record in DB for location: {location}...", flush=True)
            
            db_entry.localtime = location_data["localtime"]
            db_entry.temp_c = current["temp_c"]
            db_entry.temp_f = current["temp_f"]
            db_entry.condition = current["condition"]["text"]
            
            # Update tables, return nothing here
            for day, forecast_day in zip(db_entry.forecasts, forecast):
                # forecast_day = forecast[i]
                
                day.date = datetime.fromisoformat(forecast_day["date"])
                day.maxtemp_c = forecast_day["day"]["maxtemp_c"]
                day.mintemp_c = forecast_day["day"]["mintemp_c"]
                day.maxtemp_f = forecast_day["day"]["maxtemp_f"]
                day.mintemp_f = forecast_day["day"]["mintemp_f"]
                day.avgtemp_c = forecast_day["day"]["avgtemp_c"]
                day.avgtemp_f = forecast_day["day"]["avgtemp_f"]
                day.condition = forecast_day["day"]["condition"]["text"]
                
                for j, (hour, hour_data) in enumerate(zip(day.hours, forecast_day["hour"])):
                    forecast_hour = forecast_day["hour"]
                    if j * 4 >= len(forecast_hour):
                        break
                    hour_data = forecast_hour[j*4]
                    
                    hour.time = datetime.fromisoformat(hour_data["time"])
                    hour.temp_c = hour_data["temp_c"]
                    hour.temp_f = hour_data["temp_f"]
                    hour.condition = hour_data["condition"]["text"]
                        
            db.commit()
            cache_weather_entry = db_entry
            
            print(f"Updated existing forecast DB record for location: {location}", flush=True)
            
            
        else:
            print(f"Creating new forecast record in DB for location: {location}", flush=True)
            
            # Create new Weather entry
            weather_entry = models.Weather(
                location_name=location_data["name"],
                region=location_data["region"],
                country=location_data["country"],
                latitude=location_data["lat"],
                longitude=location_data["lon"],
                timezone=location_data["tz_id"],
                localtime=datetime.fromisoformat(location_data["localtime"]),
                temp_c=current["temp_c"],
                temp_f=current["temp_f"],
                condition=current["condition"]["text"]
            )
            
            for day in forecast:
                
                forecast_day_entry = models.ForecastDay(
                    date=datetime.fromisoformat(day["date"]),
                    maxtemp_c=day["day"]["maxtemp_c"],
                    mintemp_c=day["day"]["mintemp_c"],
                    maxtemp_f=day["day"]["maxtemp_f"],
                    mintemp_f=day["day"]["mintemp_f"],
                    avgtemp_c=day["day"]["avgtemp_c"],
                    avgtemp_f=day["day"]["avgtemp_f"],
                    condition=day["day"]["condition"]["text"]
                )
                
                for j, hour_data in enumerate(day["hour"]):
                    if j % 4 != 0:
                        continue
                    forecast_hour_entry = models.ForecastHour(
                        time=datetime.fromisoformat(hour_data["time"]),
                        temp_c=hour_data["temp_c"],
                        temp_f=hour_data["temp_f"],
                        condition=hour_data["condition"]["text"]
                    )
                    forecast_day_entry.hours.append(forecast_hour_entry)
                    
                weather_entry.forecasts.append(forecast_day_entry)
                    
            db.add(weather_entry)
            db.commit()
            
            cache_weather_entry = weather_entry
            # db.refresh(weather_entry)
            
        # Add to cache. This ensures that updated or new DB entries are found in cache, ensuring freshness.
        cache_data = utils.serialize_weather_data(cache_weather_entry)
        
        redis_client.setex(location_forecast_key, time=3600, value=json.dumps(cache_data))

        return data
    return get_forecast()