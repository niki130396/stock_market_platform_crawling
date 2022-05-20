import os
import psycopg2

connection_kwargs = {
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT"),
    "database": os.environ.get("POSTGRES_DB"),
}


def get_db_connection():
    connection = psycopg2.connect(**connection_kwargs)
    connection.set_session(autocommit=True)
    return connection
