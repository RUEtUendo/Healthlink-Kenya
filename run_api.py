import threading
import uvicorn
import time

def start_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="error")

def launch():
    thread = threading.Thread(target=start_fastapi, daemon=True)
    thread.start()
    time.sleep(2)  # give FastAPI time to start
