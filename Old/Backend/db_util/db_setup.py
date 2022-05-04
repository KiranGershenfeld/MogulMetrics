import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode="require")
DB_NAME = "MOGUL_METRICS"

tables = {}
tables["live_streams"] = """
    live_streams(
        CHANNEL_ID STRING,
        CHANNEL_NAME STRING,
        IS_LIVE BOOL,
        LOG_TIME TIMESTAMP
    )
"""
with conn.cursor() as cur:
    # The first statement in a transaction can be retried transparently on
    # the server, so we need to add a dummy statement so that our
    # force_retry() statement isn't the first one.
    cur.execute(f"USE {DB_NAME};")

    for table_name, table_setup in tables.items():
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_setup};")
        print(f"CREATED TABLE {table_name}")

conn.commit()

    
