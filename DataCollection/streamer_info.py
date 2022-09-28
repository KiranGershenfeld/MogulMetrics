from matplotlib.image import thumbnail
import requests

import sqlalchemy
import googleapiclient.discovery
from urllib.error import HTTPError

from sqlalchemy import create_engine
from sqlalchemy import text, Table, MetaData
import datetime
import json
import os


channels = {"UCrPseYLGpNygVi34QpGNqpA": "Ludwig"}
user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
hostname = os.environ.get("DB_HOST")
database_name = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT")
cluster = os.environ.get("DB_CLUSTER")
youtube_api_key = os.environ.get("YOUTUBE_API_KEY")

if __name__ == '__main__':

    current_time = datetime.datetime.now(datetime.timezone.utc)
    current_time = datetime.datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')

    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)

    engine = create_engine(f'cockroachdb://{user}:{password}@{hostname}:{port}/mogul_metrics?sslmode=require&options=--cluster={cluster}')
    metadata_obj = MetaData()

    lsc = Table('livestream_scrape_channels', metadata_obj, autoload_with=engine)
    query = sqlalchemy.select(lsc.c.channel_id)

    with engine.connect() as conn:
        try: 
            result_proxy = conn.execute(query)
            channel_set = result_proxy.fetchall()
        except Exception as e:
            exit(0)
    
    channel_set = [tup[0] for tup in channel_set]

    for channel_id in channel_set:
        print(channel_id)
        request = youtube.channels().list(
            part="snippet, statistics",
            id=channel_id
        )

        try:
            response = request.execute()
            print(response)
            channel_name = response['items'][0]['snippet']['title']
            thumbnail_url = response['items'][0]['snippet']['thumbnails']['default']['url']
            subscribers = int(response['items'][0]['statistics']['subscriberCount'])
        except HTTPError as e:
            response = None

        stmt = lsc.insert().values(channel_id=channel_id, channel_name=channel_name, thumbnail_url=thumbnail_url, subscriber_count=subscribers, log_time=current_time)

        with engine.connect() as conn:
            res = conn.execute(stmt)
