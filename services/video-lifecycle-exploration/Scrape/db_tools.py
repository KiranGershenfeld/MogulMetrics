from turtle import reset
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy import text, Table, Column, Integer, String, MetaData, ForeignKey

import sqlalchemy.dialects

load_dotenv()

user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
hostname = os.environ.get("DB_HOST")
database_name = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT")
cluster = os.environ.get("DB_CLUSTER")

engine = create_engine(f'cockroachdb://{user}:{password}@{hostname}:{port}/mogul_metrics?sslmode=require&options=--cluster={cluster}')

def reset_tables():
    with engine.connect() as connection:
        q = connection.execute("DROP TABLE IF EXISTS video_notification_feed")
        q = connection.execute(text("""CREATE TABLE IF NOT EXISTS video_notification_feed(
                                        title VARCHAR(255),
                                        updated TIMESTAMP,
                                        notification_id VARCHAR(255),
                                        video_id VARCHAR(255),
                                        channel_id VARCHAR(255),
                                        channel_name VARCHAR(1024),
                                        content_title VARCHAR(4096),
                                        content_published TIMESTAMP,
                                        content_updated TIMESTAMP,
                                        record_timestamp TIMESTAMP
                                    );"""))
        
        q = connection.execute("DROP TABLE IF EXISTS video_view_lifecycle")
        q = connection.execute(text("""CREATE TABLE IF NOT EXISTS video_view_lifecycle(
                                        video_id VARCHAR(255),
                                        video_title VARCHAR(8192),
                                        channel_id VARCHAR(255),
                                        channel_name VARCHAR(4096),
                                        views INT,
                                        likes INT,
                                        favorites INT,
                                        comment_count INT,
                                        dislikes INT,
                                        video_duration VARCHAR(255),
                                        thumbnail_url VARCHAR(8192),
                                        date_uploaded TIMESTAMP,
                                        record_timestamp TIMESTAMP
                                    );"""))

        q = connection.execute("DROP TABLE IF EXISTS video_scrape_tasks")

        q = connection.execute(text("""CREATE TABLE IF NOT EXISTS video_scrape_tasks(
                                        video_id VARCHAR(255),
                                        scheduled_execution TIMESTAMP,
                                        prev_schedule_index INT, 
                                        task_status VARCHAR(255), 
                                        video_lifecycle_status VARCHAR(255) 
                                    );"""))

        
        print(q)
 
def reset_tasks():
    with engine.connect() as connection:
        q = connection.execute("DROP TABLE IF EXISTS video_scrape_tasks")

        q = connection.execute(text("""CREATE TABLE IF NOT EXISTS video_scrape_tasks(
                                        video_id VARCHAR(255),
                                        scheduled_execution TIMESTAMP,
                                        prev_schedule_index INT, 
                                        task_status VARCHAR(255), 
                                        video_lifecycle_status VARCHAR(255) 
                                    );"""))
    return
    
def print_video_log():
    print("PRINTING VIDEO LOG")
    with engine.connect() as connection:
        res = connection.execute(text("SELECT * FROM video_view_lifecycle"))
        print(res)
        for row in res:
            print(row)

def print_task_log():
    print("PRINTING VIDEO LOG")
    with engine.connect() as connection:
        res = connection.execute(text("SELECT * FROM video_scrape_tasks"))
        print(res)
        for row in res:
            print(row)

def print_video_log_shape():
    with engine.connect() as connection:
            res = connection.execute(text("SELECT COUNT(*) from video_view_lifecycle"))
            print(res)
            for row in res:
                print(row)

def attemt_insert():
    print("ATTEMPTING INSERT")
    with engine.connect() as connection:
        #print("TABLE HAS " + connection.query("public.video_view_lifecycle").count() + "ROWS")

        sql_command = f"""INSERT INTO public.video_view_lifecycle (video_id, video_title, log_number, channel_id, channel_name, views, likes, favorites, comment_count, dislikes, video_duration, thumbnail_url, waited_before, waiting_after, date_uploaded, record_timestamp) 
                            VALUES (
                                'H5dqjlJ23Ak',
                                '$10,000 IF SHE CAN BEAT ME ON STREAM',
                                0,
                                'UCrPseYLGpNygVi34QpGNqpA',
                                'Ludwig',
                                772131,
                                37210,
                                0,
                                721,
                                -1,
                                'PTOSJALSK',
                                'https://i.ytimg.com/vi/H5dqjlJ23Ak/default.jpg',
                                0,
                                5,
                                '2022-06-08T05:58:21Z',
                                '2022-06-08T06:58:21Z'
                            );"""
                        
        # res = connection.execute(text(sql_command))

        res = connection.execute(text("SELECT * FROM video_view_lifecycle"))
        for row in res:
            print(row)

        res = connection.execute(text("SHOW TABLES;"))
        for row in res:
            print(row)

def safe_insert_test():
    metadata_obj = MetaData()
    vvl_table = Table('video_view_lifecycle', metadata_obj, autoload_with=engine)
    stmt = vvl_table.delete().where(vvl_table.c.video_id=='test_video_safe_id')
    with engine.connect() as conn:
        res = conn.execute(stmt)
    
def remove_duplicate_tasks():
    with engine.connect() as conn:
        res = conn.execute(text("""
            WITH row_ranked AS (
                SELECT video_id, prev_schedule_index, record_timestamp
                row_number() OVER(PARITION BY video_id, prev_schedule_index ORDER BY record_timestamp ASC)
            )
            SELECT * FROM row_ranked WHERE video_id='CkoquiSnqbk'
        """))


# print_task_log()
# print_video_log()
# print_video_log_shape()
safe_insert_test()