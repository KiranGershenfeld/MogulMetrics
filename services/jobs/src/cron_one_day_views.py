#!/usr/bin/env python3

from datetime import datetime, timedelta
import os
import sys
import logging
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, exc
from common import youtube #common lib defined locally in airflow/common


def get_one_day_old_videos(engine, execution_date):
        # Define the query to select records from the "videos" table created within the past hour
    execution_date = datetime.strptime(execution_date, '%Y-%m-%d %H:%M:%S')
    stmt = text(f"""
        INSERT INTO videos_1d_tmp
        SELECT youtube_id, upload_time FROM videos
        WHERE upload_time <= '{execution_date - timedelta(days=1)}' AND
        upload_time >= '{execution_date  - timedelta(days=1, minutes=10)}';
    """)
    print(stmt)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()

def get_batch_video_views(engine):
    logger = logging.getLogger(__name__)

    client = youtube.YouTubeAPI(os.environ.get("YOUTUBE_API_KEY"))

    with engine.connect() as connection:
        records = connection.execute(text("SELECT * FROM videos_1d_tmp"))
        connection.commit()
    print(records)
    if not records:
        return

    video_views = []
    for record in records:
        video_id = record[0]
        upload_time = record[1]
        try:
            views = client.get_video_views(video_id, method='api')
        except Exception as e: 
            logger.error(f"Could not get video views for video {video_id}. Error: {e}")
            continue

        video_views.append((video_id, upload_time, views))

    print(video_views)
    with engine.connect() as connection:
        for record in video_views:
            try:
                connection.execute(text(f"INSERT INTO video_views_1d (youtube_id, upload_time, view_count) VALUES ('{record[0]}', '{record[1]}', {record[2]})"))
                connection.commit()
            except exc.IntegrityError as e:
                print(f"Video id {record[0]} already found, skipping...")
                connection.rollback()
                continue

def delete_tmp_table_task(engine):
    stmt = text("""
        DROP TABLE IF EXISTS videos_1d_tmp;
    """)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()
        return

def create_tmp_table_task(engine):
    stmt = text("""
            CREATE TABLE IF NOT EXISTS videos_1d_tmp (
                youtube_id VARCHAR(255) PRIMARY KEY,
                upload_time TIMESTAMP
            );
        """)
    with engine.connect() as connection:
        connection.execute(stmt)
        connection.commit()
            
def db_conn():
    username = os.environ.get("DB_CREDENTIALS_USERNAME")
    password = os.environ.get("DB_CREDENTIALS_PASSWORD")
    host = os.environ.get("DB_CREDENTIALS_HOST")
    port = os.environ.get("DB_CREDENTIALS_PORT")
    name = os.environ.get("DB_CREDENTIALS_NAME")

    DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{name}'
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL)

    return engine

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        execution_date = datetime.now().strftime('%Y-%m-%d 00:00:00') #Default value
    else:
        execution_date = sys.argv[1]

    print(f"executing with date {execution_date}")
    engine = db_conn()
    with engine.connect() as conn:
        print (conn.execute(text("SELECT 1")))

    print(f"Deleting tmp table...")
    delete_tmp_table_task(engine)
    time.sleep(1)

    print(f"Creating tmp table...")
    create_tmp_table_task(engine)
    time.sleep(1)
    print(f"Getting one day old videos...")
    get_one_day_old_videos(engine, execution_date)
    
    print("Getting video views...")
    get_batch_video_views(engine)