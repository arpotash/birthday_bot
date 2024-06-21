import os

import psycopg2 as pg


conn = pg.connect(
    f"dbname={os.getenv('DB_NAME')}"
    f"user={os.getenv('DB_USER')}"
    f"password={os.getenv('DB_PASSWORD')}"
    f"host={os.getenv('DB_HOST')}"
)
cur = conn.cursor()


async def db_initialize():
    query = """
    create table account (id serial primary key, first_name varchar(128), last_name varchar(128), comment text null)
    """
    cur.execute(query)
    conn.commit()
