from fastapi import FastAPI,HTTPException
from data_model import DATA
import uvicorn
from typing import List

app=FastAPI()

data_list:List[DATA] = []

@app.post('/data',response_model=DATA)
async def post_data(data:DATA):
    data_list.append(data)
    return data

@app.get('/get_data')
async def get_data(id:int):
    for data in data_list:
        if data.id == id:
            return data
    raise HTTPException(status_code=404,detail="Not Found")

@app.put('/data',response_model=DATA)
async def put_data(id:int,updated_data:DATA):
    for index,data in enumerate(data_list):
        if data.id == id:
            updated_data.id=id
            data_list[index]=updated_data
            return updated_data
    raise HTTPException(status_code=404,detail="Not Found")


@app.delete('/delete_data/{id}',response_model=DATA)
async def delete_data(id:int):
    for index,data in enumerate(data_list):
        if data.id == id:
            delete_data=data_list.pop(index)
            return delete_data
    raise HTTPException(status_code=404,detail="Not Found")
            
    
            
        
    

if __name__ == '__main__':
    uvicorn.run(app,port=5000,ssl_keyfile="key.pem",ssl_certfile="cert.pem")