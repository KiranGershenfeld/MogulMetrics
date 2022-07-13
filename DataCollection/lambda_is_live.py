from bs4 import BeautifulSoup
import psycopg2
import datetime
import requests
import requests
import json
import os

CHANNELS = {"UCrPseYLGpNygVi34QpGNqpA": "Ludwig"}
DB_NAME = "MOGUL_METRICS"

pool = None

def query_scheduled_status(soup):
    body = soup.find_all("body")[0]
    scripts = body.find_all("script")
    response = json.loads(scripts[0].string[30:-1])
        
    stream_status = response["playabilityStatus"]["status"]
    if(stream_status == "LIVE_STREAM_OFFLINE"):
        try:
            scheduled_time = response["playabilityStatus"]["liveStreamability"]["liveStreamabilityRenderer"]["offlineSlate"]["liveStreamOfflineSlateRenderer"]["scheduledStartTime"]
            return True, datetime.datetime.fromtimestamp(scheduled_time)
        except KeyError as e:
            return None, None
    elif(stream_status == "OK"):
        return False, None
    else:
        return None, None

#Checks if a YouTube channel is live given an ID
def is_channel_live(channel_id):
    query_url = f"https://www.youtube.com/channel/{channel_id}/live"

    r = requests.get(query_url)
    soup = BeautifulSoup(r._content)
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
    
    for channel_id in CHANNELS:
        is_live = is_channel_live(channel_id)
        print(channel_id, CHANNELS[channel_id], current_time, is_live)
        
        conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode="require")

        with conn.cursor() as cur:
            cur.execute(
                f"USE {DB_NAME}")
            cur.execute(
                f"INSERT INTO live_streams (CHANNEL_ID, CHANNEL_NAME, IS_LIVE, LOG_TIME) VALUES ('{channel_id}', '{CHANNELS[channel_id]}', '{is_live}', '{current_time}');"
            )
        conn.commit()

    return

if __name__ == "__main__":
    lambda_handler(None, None)