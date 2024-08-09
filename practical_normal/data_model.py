from pydantic import BaseModel

class DATA(BaseModel):
    
    id: int
    name: str
    description: str
    