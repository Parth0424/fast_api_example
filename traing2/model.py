from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'mymodel'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(String)
