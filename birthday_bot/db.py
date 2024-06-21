import os

import psycopg2 as pg


conn = pg.connect(
    f"dbname=db_bot "
    f"user=postgres "
    f"password=postgres "
    f"host=localhost"
)
cur = conn.cursor()


async def db_initialize():
    query = """
    create table account (id serial primary key, first_name varchar(128), last_name varchar(128), comment text null)
    """
    cur.execute(query)
    conn.commit()
