from fastapi import FastAPI
import time
import asyncio
from datetime import datetime

app = FastAPI()

# Synchronous function with detailed logging
def some_sync_function():
    print(f"Sync function start: {datetime.now()}")
    time.sleep(10)  # Simulating a blocking, time-consuming task
    print(f"Sync function end: {datetime.now()}")

# Asynchronous function with detailed logging
async def some_async_function():
    print(f"Async function start: {datetime.now()}")
    await asyncio.sleep(5)  # Simulating a non-blocking I/O operation
    print(f"Async function end: {datetime.now()}")

@app.get("/sync")
def read_data_sync():
    print(f"Sync function start: {datetime.now()}")
    time.sleep(550)  # Simulating a blocking, time-consuming task
    print(f"Sync function end: {datetime.now()}")
    return {"message": "Synchronous endpoint"}

@app.get("/async")
async def read_data_async():
    await some_async_function()
    return {"message": "Asynchronous endpoint"}
