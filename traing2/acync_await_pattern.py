# # import asyncio

# # async def fetch_data():
# #     await asyncio.sleep(2)  # Simulate an I/O-bound operation
# #     return "Data fetched"

# # async def main():
# #     data = await fetch_data()
# #     print(data)

# # # Run the main coroutine
# # asyncio.run(main())

# from databases import Database

# DATABASE_URL = "sqlite:///./example.db"
# database = Database(DATABASE_URL)

# async def connect_to_db():
#     await database.connect()

# async def disconnect_from_db():
#     await database.disconnect()
    
    
# from fastapi import FastAPI

# app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     await connect_to_db()

# @app.on_event("shutdown")
# async def shutdown():
#     await disconnect_from_db()

# @app.get("/items/")
# async def read_items():
#     query = "SELECT * FROM items"
#     return await database.fetch_all(query)


# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# engine = create_engine(DATABASE_URL)
# metadata = MetaData()

# items = Table(
#     "items",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("description", String)
# )

# # Create the database tables
# metadata.create_all(engine)


# @app.post("/items/")
# async def create_item(name: str, description: str):
#     query = items.insert().values(name=name, description=description)
#     await database.execute(query)
#     return {"name": name, "description": description}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     query = items.select().where(items.c.id == item_id)
#     return await database.fetch_one(query)

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, name: str, description: str):
#     query = items.update().where(items.c.id == item_id).values(name=name, description=description)
#     await database.execute(query)
#     return {"id": item_id, "name": name, "description": description}

# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     query = items.delete().where(items.c.id == item_id)
#     await database.execute(query)
#     return {"id": item_id}


from fastapi import FastAPI
import asyncio

app = FastAPI()

# An endpoint that uses the async function
@app.get("/async_task")
def async_task():
    print("hello")
    asyncio.sleep(5)
    print("bye")


