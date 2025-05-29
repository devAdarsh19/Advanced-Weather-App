# Weather App with System Design Principles

## Requirements 
- fastapi
- uvicorn
- redis
- PostgreSQL

Install requirements with
```
pip install -r requirements.txt
```

## Running the project
### Redis install
Use Homebrew on Mac or your package manager on Linux

For Windows, install WSL (Windows Subsystem for Linux) using help from these links:
- [WSL Microsoft Page](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Redis with FastAPI](https://www.youtube.com/watch?v=6nY-kci1rlo)

Create virtual environment:
```
python -m venv <env_name>
<env_name>/Scripts/activate
```

Install requirements with
```
pip install -r requirements.txt
```

Run FastAPI app:
```
uvicorn main:app --reload
```

## Principles Applied
### Latency
Using Redis for application level caching, i.e., a cache memory between the application and PostreSQL database.

Pipeline:
- Hit weather API to retrieve weather information of desired location. Store the data in DB + cache it using Redis with a TTL of 30 minutes.
- Using location as the key, if it exists in cache, it's a cache hit; else cache miss.
- In case of cache miss, query the database. Database is kept fresh using a time difference check. If the entry is stale, the external API is hit, necessary fields updated and cache updated.
