import os
import sys
import psycopg2
import time


def connect(conn_string: str, retry_num: int = 0):
    conn = None

    while conn is None:
        try:
            conn = psycopg2.connect(conn_string)
        except psycopg2.OperationalError as e:
            if retry_num > 5:
                raise e
            time.sleep(1)
            conn = connect(conn_string, retry_num + 1)

    return conn


DB_NAME = os.getenv('TAIGA_DB_NAME')
DB_HOST = os.getenv('TAIGA_DB_HOST')
DB_USER = os.getenv('TAIGA_DB_USER')
DB_PASS = os.getenv('TAIGA_DB_PASSWORD')

conn_string = (
    "dbname='" + DB_NAME +
    "' user='" + DB_USER +
    "' host='" + DB_HOST +
    "' password='" + DB_PASS + "'")
print("Connecting to database:\n" + conn_string)

exception = None
conn = connect(conn_string)
cur = conn.cursor()

cur.execute("select * from information_schema.tables where table_name=%s", ('django_migrations',))
exists = bool(cur.rowcount)

if exists is False:
    print("Database does not appear to be setup.")
    sys.exit(2)
