from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import redis
from redis.cache import CacheConfig
import json
from typing import Annotated, List
import requests
import os
import time
from datetime import datetime, timedelta

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/weather")
def get_weather(location_q: str, db: db_dependency):
    start_time = time.time()
    
    # Check for cached data in redis
    location_key = f"key:{location_q.strip().lower()}"
    
    cached = redis_client.get(location_key)
    if cached:
        print(f"Cache hit for location: {location_q}")
        
        ######## Latency calculation ########
        end_time = time.time()
        duration = round((end_time - start_time) * 1000, 2)
        print(f"Latency (ms) for cache hit: {duration} ms")
        
        return json.loads(cached)
    
    ##############################################################################
    # Check DB to retrieve data if cache miss
    db_entry = (
        db.query(models.Weather)
        .filter(models.Weather.location_name.ilike(location_q))
        .order_by(models.Weather.localtime.desc())
        .first()
    )
    
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
        
        ######## Latency calculation ########
        end_time = time.time()
        duration = round((end_time  - start_time) * 1000, 2)
        print(f"DB queried for location: {location_q}")
        print(f"Latency (ms) for DB query: {duration} ms")
        
        
        response["latency (ms)"] = duration
        
        return response
    
    #######################################################################
    # Hit the Free Weather API endpoint
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
        
        print(f"Updated existing DB record for location: {location_q}")
    else:
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
    
    ######## Latency calculation ########
    end_time = time.time()
    duration = round((end_time - start_time) * 1000, 2)
    print(f"Latency (ms): {duration} ms")
    
    data["latency_ms"] = duration

    print(f"Hitting external API for location : {location_q}")
    return data


@app.get("/forecast")
def get_forecast(location: str, days: int):
    res = requests.get(url=f"{WEATHER_API_URL}/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}")

    if res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch forecast data")

    return res.json()