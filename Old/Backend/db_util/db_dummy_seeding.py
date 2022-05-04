import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode="require")
DB_NAME = "MOGUL_METRICS"

table_name = "live_stream_dummy"
table_setup_command = """
    live_stream_dummy(
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

    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_setup_command};")
    print(f"CREATED TABLE {table_name}")

    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-02-28 13:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-02-28 14:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-02-28 15:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-02-28 16:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 14:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 15:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 15:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 15:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 15:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 16:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 16:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 16:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false', '2022-02-28 16:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 17:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 17:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 17:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 17:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 18:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 18:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 18:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 18:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 19:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 19:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 19:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 19:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 20:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 21:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 22:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 23:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'false','2022-02-28 24:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-01 14:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-01 15:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-01 16:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-02 12:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-02 13:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-03 07:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-05 07:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-05 05:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-05 04:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-05 03:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-05 07:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-07 05:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-08 04:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-09 03:00:00');")
    cur.execute(f"INSERT INTO live_stream_dummy (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('dummy_id', 'Ludwig', 'true', '2022-03-10 03:00:00');")

conn.commit()

    
