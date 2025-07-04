import json
import datetime
import inspect
from functools import wraps
import time
from models import Weather


def serialize_weather_data(db_entry: Weather):
    """
    Creates a JSON-compatible response if db_entry is found in the database.
    Also dumped in cache, post retrieval.

    Args:
        db_entry (Weather): Object returned from the database query.

    Returns:
        _type_: A dictionary representation of the Weather entry with forecasts.
    """

    try:
        return json.dumps(
            {
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
            }
        )
    except AttributeError as e:
        print(f"[ERROR] Error while weather serialization (NoneType object passed). Try again: \n{e}")
        raise

def serialize_forecast_data(db_entry: Weather):
    """
    Serializes a Weather database entry into a JSON-compatible dictionary.
    
    Args:
        db_entry (Weather): The Weather database entry to serialize.
        
    Returns:
        dict: A dictionary representation of the Weather entry.
    """
    
    try:
        return json.dumps({
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
        })
    except AttributeError as e:
        print(f"[ERROR] Error while forecast serialization (NoneType object passed). Try again: \n{e}")
        raise


def logger(func):
    """
    A logging decorator to log endpoint output, errors and execution times

    Args:
        func (_type_): A function to pass that is executed within the wrapper.

    Raises:
        ValueError: If the returned response is not a string or dictionary.

    Returns:
        _type_: Wrapper function
    """
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            print(f" ----- Calling '{func.__name__}' ----- ")
            print(f"Arguments: args={args} | kwargs={kwargs}")
            start_time = time.time()
            
            result = None
            result_dict = {}
            
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] Error while function execution: {e}")
                raise
                
            try:
                if isinstance(result, str):
                    result_dict = json.loads(result)
                    print(f"[LOGGER] Function {func.__name__} returned {result}")
                elif isinstance(result, dict):
                    result_dict = result
                    print(f"[LOGGER] Function {func.__name__} returned {result}")
                else:
                    raise ValueError(f"Incorrect return type from function. Expected str or dict. Recieved {type(result)}")
            except Exception as e:
                print(f"[ERROR] Error while parsing JSON: {e}")
            # finally:
            
            end_time = time.time()
            result_dict["latency_ms"] = round((end_time - start_time) * 1000, 2)
                
            print(f"[LOGGER] Endpoint latency (in ms) for '{func.__name__}': {round((end_time - start_time) * 1000, 2)} ms")
            return result_dict  
        return async_wrapper
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f" ----- Calling '{func.__name__}' ----- ")
            print(f"Arguments: args={args} | kwargs={kwargs}")
            start_time = time.time()
            
            result = None
            result_dict = {}
            
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] Error while function execution: {e}")
                raise
                
            try:
                if isinstance(result, str):
                    result_dict = json.loads(result)
                    print(f"[LOGGER] Function {func.__name__} returned {result}")
                elif isinstance(result, dict):
                    result_dict = result
                    print(f"[LOGGER] Function {func.__name__} returned {result}")
                else:
                    raise ValueError(f"Incorrect return type from function. Expected str or dict. Recieved {type(result)}")
            except Exception as e:
                print(f"[ERROR] Error while parsing JSON: {e}")
            # finally:
            
            end_time = time.time()
            result_dict["latency_ms"] = round((end_time - start_time) * 1000, 2)
                
            print(f"[LOGGER] Endpoint latency (in ms) for '{func.__name__}': {round((end_time - start_time) * 1000, 2)} ms")
            return result_dict  
        
            
        return wrapper
