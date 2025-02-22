import sqlite3
from config.config import DATABASE_FILE, REDIS_HOST, REDIS_PORT
import redis

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_redis_connection():
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return redis_client
