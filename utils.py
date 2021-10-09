import psycopg2
import logging
from urllib.parse import urlparse

from config import DATABASE_URL


def connect_to_db():
    result = urlparse(DATABASE_URL)
    try:
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
    except psycopg2.OperationalError:
        logging.error("Can't connect to the database with given DATABASE_URL={}\n".format(db_url))
        return None
    else:
        return conn
