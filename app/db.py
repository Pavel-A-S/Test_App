import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def require(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value

DB_CONFIG = {
    "host": require("MYSQL_HOST"),
    "user": require("MYSQL_USER"),
    "password": require("MYSQL_PASSWORD"),
    "database": require("MYSQL_DB"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)