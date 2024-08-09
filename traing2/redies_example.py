from fastapi import FastAPI, Depends
from redis import Redis
from pydantic import BaseModel
import hashlib

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, db=0)

class Item(BaseModel):
    name: str
    description: str

def generate_cache_key(item: Item):
    return hashlib.md5(item.json().encode()).hexdigest()

@app.post("/items/")
async def create_item(item: Item):
    cache_key = generate_cache_key(item)
    complex_result = f"Processed {item.name} with {item.description}"

    redis_client.setex(cache_key, 3600, complex_result)  # Cache for 1 hour
    return {"cached": False, "item": complex_result}

@app.put("/items/")
async def update_item(item: Item):
    cache_key = generate_cache_key(item)
    complex_result = f"Updated {item.name} with {item.description}"

    redis_client.setex(cache_key, 3600, complex_result)  # Cache for 1 hour
    return {"updated": True, "item": complex_result}

@app.get("/items/")
async def get_item(item: Item):
    cache_key = generate_cache_key(item)
    cached_item = redis_client.get(cache_key)

    if cached_item:
        return {"cached": True, "item": cached_item}

    # Fetch from database (simulated here)
    complex_result = f"Fetched {item.name} with {item.description}"
    redis_client.setex(cache_key, 3600, complex_result)  # Cache for 1 hour
    return {"cached": False, "item": complex_result}

@app.delete("/items/")
async def delete_item(item: Item):
    cache_key = generate_cache_key(item)
    redis_client.delete(cache_key)
    return {"deleted": True}
