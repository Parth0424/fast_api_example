from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    debug = os.getenv("DEBUG")
    return {"debug": debug}


# Advanced Configuration
# Setting host, port, and log level:

# bash
# Copy code
# # Run Uvicorn with custom host, port, and log level
# uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info
# Enabling hot reload for development:

# bash
# Copy code
# # Use the --reload flag for auto-reloading in development
# uvicorn main:app --reload
# Configuring workers and concurrency settings:

# bash
# Copy code
# # Use the --workers flag to set the number of worker processes
# uvicorn main:app --workers 4


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     import time
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
