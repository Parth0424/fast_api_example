from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def background_task(name: str):
    time.sleep(10)
    print(f"Hello {name}")

@app.post("/send-email/")
async def send_email(name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task, name)
    return {"message": "Email sent in the background"}
