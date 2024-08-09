from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

# Define a data model for items including user_id
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    user_id: int  # Adding user_id to the item model

# In-memory store for items
items: Dict[int, Item] = {}

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Endpoint to get item by ID, with optional query parameter
# Example URL: http://127.0.0.1:8000/items/1?q=somequery
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    item = items.get(item_id)
    if item:
        return {"item_id": item_id, "item": item, "q": q}
    raise HTTPException(status_code=404, detail="Item not found")

# Endpoint to create a new item
# Example URL: http://127.0.0.1:8000/items/
# Example body: { "name": "Item1", "description": "A sample item", "price": 19.99, "tax": 1.99, "user_id": 1 }
@app.post("/items/")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# Endpoint to delete an item by ID
# Example URL: http://127.0.0.1:8000/items/1
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# Endpoint to update an item by ID
# Example URL: http://127.0.0.1:8000/items/1
# Example body: { "name": "Updated Item", "description": "Updated description", "price": 29.99, "tax": 2.99, "user_id": 2 }
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id in items:
        items[item_id] = item
        return {"item_id": item_id, "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

# Endpoint to partially update an item by ID
# Example URL: http://127.0.0.1:8000/items/1
# Example query parameters: ?name=NewName&description=NewDescription&price=39.99&tax=3.99
@app.patch("/items/{item_id}")
def patch_item(item_id: int, name: Optional[str] = None, description: Optional[str] = None, price: Optional[float] = None, tax: Optional[float] = None):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if description is not None:
        item.description = description
    if price is not None:
        item.price = price
    if tax is not None:
        item.tax = tax
    
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# Endpoint to get user by ID
# Example URL: http://127.0.0.1:8000/users/1
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# Endpoint to search for items with optional query parameters
# Example URL: http://127.0.0.1:8000/search/?query=searchterm&max_price=100.0
@app.get("/search/")
def search_items(query: str = None, max_price: float = None):
    results = {"query": query, "max_price": max_price}
    return results

# Endpoint to get items of a specific user with pagination
# Example URL: http://127.0.0.1:8000/users/1/items/?skip=0&limit=10
@app.get("/users/{user_id}/items/")
def get_user_items(user_id: int, skip: int = 0, limit: int = 10):
    user_items = {item_id: item for item_id, item in items.items() if item.user_id == user_id}
    paginated_items = dict(list(user_items.items())[skip: skip + limit])
    return {"user_id": user_id, "items": paginated_items, "skip": skip, "limit": limit}


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field, validator, root_validator
# from typing import Optional
# from enum import Enum

# app = FastAPI()

# # Enum for item types with constrained values
# class ItemType(str, Enum):
#     consumable = "consumable"
#     durable = "durable"

# # Pydantic model for request and response data with validation
# class Item(BaseModel):
#     name: str = Field(..., min_length=1, max_length=100)
#     description: Optional[str] = Field(None, max_length=300)
#     price: float = Field(..., gt=0)  # Price must be greater than 0
#     tax: Optional[float] = Field(None, ge=0)  # Tax must be greater than or equal to 0
#     type: ItemType  # Using Enum for constrained values
#     user_id: int


#     # Root validator to check that tax does not exceed price
#     @root_validator(pre=True)
#     def check_price_and_tax(cls, values):
#         price = values.get('price')
#         tax = values.get('tax')
#         if tax is not None and price is not None and tax > price:
#             raise ValueError('Tax cannot be greater than the price')
#         return values

# # In-memory store for items
# items = {}

# # Endpoint to create a new item
# # Example URL: http://127.0.0.1:8000/items/
# # Example Body:
# # {
# #   "name": "Sample Item",
# #   "description": "This is a sample item.",
# #   "price": 10.99,
# #   "tax": 0.99,
# #   "type": "consumable",
# #   "user_id": 1
# # }
# @app.post("/items/", response_model=Item)
# def create_item(item: Item):
#     item_id = len(items) + 1
#     items[item_id] = item
#     return item

# # Endpoint to get an item by ID
# # Example URL: http://127.0.0.1:8000/items/1
# @app.get("/items/{item_id}", response_model=Item)
# def get_item(item_id: int):
#     if item_id in items:
#         return items[item_id]
#     raise HTTPException(status_code=404, detail="Item not found")

# # Endpoint to update an item by ID
# # Example URL: http://127.0.0.1:8000/items/1
# # Example Body:
# # {
# #   "name": "Updated Item",
# #   "description": "Updated description.",
# #   "price": 19.99,
# #   "tax": 1.99,
# #   "type": "durable",
# #   "user_id": 2
# # }
# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: int, item: Item):
#     if item_id in items:
#         items[item_id] = item
#         return item
#     raise HTTPException(status_code=404, detail="Item not found")

# # Endpoint to partially update an item by ID
# # Example URL: http://127.0.0.1:8000/items/1?name=UpdatedName
# # Example Query Parameters: ?name=UpdatedName&price=29.99
# @app.patch("/items/{item_id}")
# def patch_item(item_id: int, name: Optional[str] = None, description: Optional[str] = None, price: Optional[float] = None, tax: Optional[float] = None):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")

#     item = items[item_id]
#     if name is not None:
#         item.name = name
#     if description is not None:
#         item.description = description
#     if price is not None:
#         item.price = price
#     if tax is not None:
#         item.tax = tax

#     items[item_id] = item
#     return item

# # Endpoint to delete an item by ID
# # Example URL: http://127.0.0.1:8000/items/1
# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     if item_id in items:
#         del items[item_id]
#         return {"message": "Item deleted"}
#     raise HTTPException(status_code=404, detail="Item not found")

# # Endpoint to search for items with optional query parameters
# # Example URL: http://127.0.0.1:8000/search/?query=sample&max_price=20.0
# @app.get("/search/")
# def search_items(query: Optional[str] = None, max_price: Optional[float] = None):
#     results = {"query": query, "max_price": max_price}
#     filtered_items = {id: item for id, item in items.items() if (query is None or query.lower() in item.name.lower()) and (max_price is None or item.price <= max_price)}
#     return {"results": filtered_items}

# # Endpoint to get items for a specific user with pagination
# # Example URL: http://127.0.0.1:8000/users/1/items/?skip=0&limit=10
# @app.get("/users/{user_id}/items/")
# def get_user_items(user_id: int, skip: int = 0, limit: int = 10):
#     user_items = {item_id: item for item_id, item in items.items() if item.user_id == user_id}
#     paginated_items = dict(list(user_items.items())[skip: skip + limit])
#     return {"user_id": user_id, "items": paginated_items, "skip": skip, "limit": limit}
