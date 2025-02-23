from config.config import DB_QUERIES_FILE
from db.connection import get_db_connection, get_redis_connection
import json


def get_query_from_sql_file(query_name: str):
    with open(DB_QUERIES_FILE, "r") as f:
        sql_script = f.read()

    queries = {}
    current_query = None
    for line in sql_script.split("\n"):
        line = line.strip()
        if line.startswith("--"):  # Comment line (query name)
            current_query = line[2:].strip()
            queries[current_query] = []
        elif current_query:
            queries[current_query].append(line)

    # Join the extracted query lines
    return "\n".join(queries.get(query_name, []))



def ExecuteQueryInDB(query: str, params):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    affected_rows = cursor.rowcount
    conn.commit()
    conn.close()
    print("affected_rows:: ", affected_rows)
    return True if affected_rows > 0 else False


def FetchOneInDB(query: str, params):
    conn = get_db_connection()
    cursor = conn.cursor() 
    cursor.execute(query, params)
    data = cursor.fetchone()
    column_names = [description[0] for description in cursor.description]
    if data and len(data) > 0:
        data = dict(zip(column_names, data))    
    else:
        data = {}
    conn.close() 
    return data

def FetchAllFromDB(query: str, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    if cursor.rowcount:
        result = [dict(zip(column_names, row)) for row in data]
    else:
        result = []
    cursor.close()
    conn.close()
    return result



def SetDataInRedis(dataToInsertInQueue, priority):
    print("Inside redis", dataToInsertInQueue, priority)
    redis_client = get_redis_connection()
    redis_client.zadd("deployment_queue", {json.dumps(dataToInsertInQueue): priority}) 


def GetRedisData():
    redis_client = get_redis_connection()
    deployment_data = redis_client.zrevrange("deployment_queue", 0, 1000, withscores=True)
    # print("deployment_data:: ", deployment_data)
    return deployment_data

def RemoveFromRedis(deployment_json):
    redis_client = get_redis_connection()
    redis_client.zrem("deployment_queue", deployment_json)

