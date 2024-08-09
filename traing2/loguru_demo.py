from fastapi import FastAPI
from loguru import logger

app = FastAPI()

# Configure Loguru
logger.add("file.log", rotation="1 MB", retention="10 days", level="DEBUG")

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}



# custome
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()
# Example items database
items_db = {
    1: {"name": "item1", "description": "Description of item 1"},
    2: {"name": "item2", "description": "Description of item 2"},
}

# Define a custom exception
class ItemNotFound(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

# Register a custom error handler
@app.exception_handler(ItemNotFound)
async def item_not_found_handler(request: Request, exc: ItemNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item with ID {exc.item_id} not found"}
    )

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items_db:
        raise ItemNotFound(item_id=item_id)
    return {"item": items_db[item_id]}
