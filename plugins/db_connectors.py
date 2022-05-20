import os
import psycopg2
import sqlite3


connection_kwargs = {
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT"),
    "database": os.environ.get("POSTGRES_DB"),
}


def get_db_connection():
    if not os.environ.get("IS_TEST_ENVIRONMENT") == "true":
        connection = psycopg2.connect(**connection_kwargs)
        connection.set_session(autocommit=True)
    else:
        connection = sqlite3.connect("stock_market_platform")
    return connection
