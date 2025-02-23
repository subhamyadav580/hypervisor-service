DATABASE_FILE = "test.db"
INIT_FILE = "db/init.sql"
DB_QUERIES_FILE = "db/queries.sql"


SECRET_KEY = "6UfD7GWh8C1Ju5SOLdzZnapIMlZI10cW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expires in 1 hour


REDIS_HOST = "redis" #if using docker redis inside docker then user `redis` as host if not then `localhost`
REDIS_PORT = 6379