from fastapi import FastAPI, APIRouter
from db.connection import get_db_connection
from config.config import INIT_FILE
from handlers.hypervisor_handlers import router
from services.scheduler_service import scheduler_worker
import threading
import pytest

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    print("Hypervisor service is starting")
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(INIT_FILE, "r") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()



    # Start the scheduler worker in a separate thread
    scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
    scheduler_thread.start()
