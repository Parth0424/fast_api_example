# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE = 'example.db'

class Item(BaseModel):
    name: str
    description: str = None

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
#http://127.0.0.1:8000/items/
@app.post("/items/")
async def create_item(item: Item):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO items (name, description) VALUES (?, ?)', (item.name, item.description))
    conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = c.fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item["id"], "name": item["name"], "description": item["description"]}

#http://127.0.0.1:8000/items/1
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE items SET name = ?, description = ? WHERE id = ?', (item.name, item.description, item_id))
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully"}
