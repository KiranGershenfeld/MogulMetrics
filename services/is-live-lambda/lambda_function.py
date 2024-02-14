#DEPLOY CMD: python3 lambda_packager.py . True IS_LIVE_ARN

from bs4 import BeautifulSoup
import datetime
import requests
import requests
import json
import os

from urllib.error import HTTPError

import sqlalchemy
import googleapiclient.discovery
from sqlalchemy import create_engine
from sqlalchemy import text, Table, MetaData
from dotenv import load_dotenv

load_dotenv()
channels = {"UCrPseYLGpNygVi34QpGNqpA": "Ludwig"}
user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
hostname = os.environ.get("DB_HOST")
database_name = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT")
cluster = os.environ.get("DB_CLUSTER")
db_url = os.environ.get("DATABASE_URL")
youtube_api_key = os.environ.get("YOUTUBE_API_KEY")

def get_youtube_page(channel_id):
    query_url = f"https://www.youtube.com/channel/{channel_id}/live"

    r = requests.get(query_url)
    soup = BeautifulSoup(r._content)
    return soup

def query_scheduled_status(soup):
    body = soup.find_all("body")[0]
    scripts = body.find_all("script")
    response = json.loads(scripts[0].string[30:-1])
        
    stream_status = response["playabilityStatus"]["status"]
    if(stream_status == "LIVE_STREAM_OFFLINE"):
        try:
            scheduled_time = response["playabilityStatus"]["liveStreamability"]["liveStreamabilityRenderer"]["offlineSlate"]["liveStreamOfflineSlateRenderer"]["scheduledStartTime"]
            print(scheduled_time)
            return True, datetime.datetime.fromtimestamp(int(scheduled_time))
        except KeyError as e:
            return None, None
    elif(stream_status == "OK"):
        return False, None
    else:
        return None, None

#Checks if a YouTube channel is live given an ID
def is_channel_live(soup, channel_id):
    query_url = f"https://www.youtube.com/channel/{channel_id}/live"
    redirect = soup.find('link', {'rel': 'canonical'})["href"]

    stripped_query_url = query_url.split("/live")[0]
    is_redirected = stripped_query_url != redirect

    if is_redirected:
        #If there was a redirect the channel is either live, or scheduled
        #Parse dom for actual live or just scheduled.
        is_scheduled, schedule_time = query_scheduled_status(soup)
        if(is_scheduled is None):
            return False
        #If the stream is redirecting and not scheduled, it is live
        elif(is_scheduled == False):
            return True
        elif(is_scheduled == True):
            return False
    else:
        return False

def lambda_handler(event, context):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    current_time = datetime.datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')
    
    engine = create_engine(db_url)
    metadata_obj = MetaData()
    
    lsc = Table('livestream_scrape_channels', metadata_obj, autoload_with=engine)
    query = sqlalchemy.select(lsc.c.channel_id, lsc.c.channel_name).distinct(lsc.c.channel_id).filter(lsc.c.channel_name.isnot(None))

    with engine.connect() as conn:
        try: 
            result_proxy = conn.execute(query)
            channel_set = result_proxy.fetchall()
        except Exception as e:
            return

    for channel_id, channel_name in channel_set:
        soup = get_youtube_page(channel_id)
        is_live = is_channel_live(soup, channel_id)
        print(channel_id, channel_name, current_time, is_live)
        
        concurrent_viewers = None
        video_id = None
        stream_title = None
        thumbnail_png = None

        if(is_live):
            redirect = soup.find('link', {'rel': 'canonical'})["href"]
            video_id = redirect.split("youtube.com/watch?v=")[1]
            
            api_service_name = "youtube"
            api_version = "v3"
            youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)
            request = youtube.videos().list(
                part="snippet, liveStreamingDetails, statistics",
                id=video_id
            )
        
            try:
                response = request.execute()
                concurrent_viewers = response['items'][0]['liveStreamingDetails']['concurrentViewers']
                video_id = response['items'][0]['id']
                stream_title = response['items'][0]['snippet']['title']
                thumbnail_png = response['items'][0]['snippet']['thumbnails']['default']['url']
            except HTTPError as e:
                response = None

        live_streams_table = Table('live_streams', metadata_obj, autoload_with=engine)
        
        stmt = live_streams_table.insert().values(channel_id=channel_id, channel_name=channel_name, is_live=is_live ,log_time=current_time, concurrent_viewers=concurrent_viewers, video_id=video_id, stream_title=stream_title, thumbnail_url=thumbnail_png)

        with engine.connect() as conn:
            res = conn.execute(stmt)

    return

if __name__ == "__main__":
    lambda_handler(None, None)