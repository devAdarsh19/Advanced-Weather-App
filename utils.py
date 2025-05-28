import json
import datetime
from models import Weather


def create_forecast_response(db_entry: Weather):
    forecast_days = []
    for day in db_entry.forecasts:
        forecast_hours = []
        for hour in day.hours:
            forecast_hours.append({
                "time": hour.time.isoformat(),
                "temp_c": hour.temp_c,
                "temp_f": hour.temp_f,
                "condition": hour.condition.text
            })
                    
        forecast_days.append({
            "date": day.date.isoformat(),
            "maxtemp_c": day.maxtemp_c,
            "mintemp_c": day.mintemp_c,
            "maxtemp_f": day.maxtemp_f,
            "mintemp_f": day.mintemp_f,
            "avgtemp_c": day.avgtemp_c,
            "avgtemp_f": day.avgtemp_f,
            "condition": day.condition.text,
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