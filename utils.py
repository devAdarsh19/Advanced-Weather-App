import json
import datetime
from functools import wraps
import time
from models import Weather


def create_forecast_response(db_entry: Weather):
    """
    Creates a JSON-compatible response if db_entry is found in the database.
    Also dumped in cache, post retrieval.

    Args:
        db_entry (Weather): Object returned from the database query.

    Returns:
        _type_: A dictionary representation of the Weather entry with forecasts.
    """
    forecast_days = []
    for day in db_entry.forecasts:
        forecast_hours = []
        for hour in day.hours:
            forecast_hours.append({
                "time": hour.time.isoformat(),
                "temp_c": hour.temp_c,
                "temp_f": hour.temp_f,
                "condition": hour.condition
            })
                    
        forecast_days.append({
            "date": day.date.isoformat(),
            "maxtemp_c": day.maxtemp_c,
            "mintemp_c": day.mintemp_c,
            "maxtemp_f": day.maxtemp_f,
            "mintemp_f": day.mintemp_f,
            "avgtemp_c": day.avgtemp_c,
            "avgtemp_f": day.avgtemp_f,
            "condition": day.condition,
            "hours": forecast_hours
        })
        
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
        "condition": db_entry.condition,
        "forecast_days": forecast_days
    }
    
    return response

def serialize_weather_data(db_entry: Weather):
    """
    Serializes a Weather database entry into a JSON-compatible dictionary.
    
    Args:
        db_entry (Weather): The Weather database entry to serialize.
        
    Returns:
        dict: A dictionary representation of the Weather entry.
    """
    
    return {
        "location_name": db_entry.location_name,
        "region": db_entry.region,
        "country" : db_entry.country,
        "latitude": db_entry.latitude,
        "longitude": db_entry.longitude,
        "timezone": db_entry.timezone,
        "localtime": db_entry.localtime.isoformat(),
        "temp_c": db_entry.temp_c,
        "temp_f": db_entry.temp_f,
        "condition": db_entry.condition,
        "forecasts": [
            {
                "date": day.date.isoformat(),
                "maxtemp_c": day.maxtemp_c,
                "mintemp_c": day.mintemp_c,
                "maxtemp_f": day.maxtemp_f,
                "mintemp_f": day.mintemp_f,
                "avgtemp_c": day.avgtemp_c,
                "avgtemp_f": day.avgtemp_f,
                "condition": day.condition,
                "hours": [
                    {
                        "time": hour.time.isoformat(),
                        "temp_c": hour.temp_c,
                        "temp_f":hour.temp_f,
                        "condition": hour.condition
                    }
                    for hour in day.hours
                ]
            }
            for day in db_entry.forecasts
        ]
    }
    
    
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f" ----- Calling '{func.__name__}' ----- ")
        print(f"Arguments: args={args} | kwargs={kwargs}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            print(f"Function {func.__name__} returned: \n{result}")
            return result
        except Exception as e:
            print(f"Error while execution: {e}")
            raise
        finally:
            end_time = time.time()
            print(f"Endpoint latency (in ms) for '{func.__name__}': {round((end_time - start_time) * 1000, 2)} ms")
            result["latency_ms"] = round((end_time - start_time) * 1000, 2)
            
    return wrapper  
    