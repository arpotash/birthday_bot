import os

import psycopg2 as pg


conn = pg.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cur = conn.cursor()


async def db_initialize():
    query = """
    create table account (id serial primary key, first_name varchar(128), last_name varchar(128), comment text null)
    """
    cur.execute(query)
    conn.commit()
