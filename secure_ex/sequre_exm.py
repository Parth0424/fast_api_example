import sqlite3
import hashlib
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
import time

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["ghghfhgfc"],  # Update this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# Rate limiting settings
RATE_LIMIT = 5  # 5 requests
RATE_LIMIT_PERIOD = 10  # per 10 seconds
rate_limit_cache = {}

# Database setup
def get_db_connection():
    conn = sqlite3.connect('example.db')
    return conn

def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_test_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)
    ''', ('admin', hashlib.sha256('password'.encode()).hexdigest(), 'admin'))
    conn.commit()
    conn.close()

create_users_table()
insert_test_user()

# Authentication function
def authenticate(credentials: HTTPBasicCredentials):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                   (credentials.username, hashlib.sha256(credentials.password.encode()).hexdigest()))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# Rate limiter function
async def rate_limiter(client_ip: str):
    current_time = time.time()

    if client_ip not in rate_limit_cache:
        rate_limit_cache[client_ip] = []

    request_times = rate_limit_cache[client_ip]
    request_times = [t for t in request_times if current_time - t < RATE_LIMIT_PERIOD]
    rate_limit_cache[client_ip] = request_times

    if len(request_times) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")

    request_times.append(current_time)

# Asynchronous handler for a sample endpoint
@app.get("/")
async def handle(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    await rate_limiter(request.client.host)
    authenticate(credentials)
    await asyncio.sleep(1)  # Simulate a slow operation
    return {"message": "Hello, world"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
