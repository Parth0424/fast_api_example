from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
async def read_root():
    time.sleep(1)  # Simulating a delay
    return {"Hello": "World"}

# To profile this application, you would run the following command in the terminal:
# python -m cProfile -o profile.prof main.py
