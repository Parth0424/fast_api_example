
from fastapi import FastAPI
from gino import Gino

app = FastAPI()

db = Gino()

app.add_event_handler("startup", db.set_bind("postgresql://user:password@localhost/dbname"))


from gino import Gino

db = Gino()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    
    
@app.post("/users/")
async def create_user(name: str, email: str):
    user = await User.create(name=name, email=email)
    return user

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = await User.get(user_id)
    return user

