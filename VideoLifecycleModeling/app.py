
import json
import logging
import os
from dotenv import load_dotenv

from flask import Flask, request, Response
import xmltodict
from xml.parsers.expat import ExpatError
from sqlalchemy import create_engine
from sqlalchemy import text
from datetime import datetime, timedelta
import pytz
import requests


logging.basicConfig(filename='./lifecycle.log')
logging.info("Logger Initialized")

load_dotenv()

app = Flask(__name__)

user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
hostname = os.environ.get("DB_HOST")
database_name = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT")
cluster = os.environ.get("DB_CLUSTER")

engine = create_engine(f'cockroachdb://{user}:{password}@{hostname}:{port}/mogul_metrics?sslmode=require&options=--cluster={cluster}')

subscriptions = {}

def write_video_notification(data):
    title = data.get("title")
    updated = data.get("updated")
    id = data.get("entry").get("id")
    video_id = data.get("entry", {}).get("yt:videoId")
    channel_id = data.get("entry", {}).get("yt:channelId")
    channel_name = data.get("entry", {}).get("author", {}).get("name")
    content_title = data.get("entry", {}).get("title")
    content_published = data.get("entry", {}).get("published")
    content_updated = data.get("entry", {}).get("updated")

    record_timestamp = datetime.utcnow()
    
    with engine.connect() as connection:
        connection.execute(text(f"""INSERT INTO video_notification_feed (title ,
                                        updated,
                                        notification_id,
                                        video_id,
                                        channel_id,
                                        channel_name,
                                        content_title,
                                        content_published,
                                        content_updated,
                                        record_timestamp)
                                        VALUES (
                                        '{title}',
                                        '{updated}',
                                        '{id}',
                                        '{video_id}',
                                        '{channel_id}',
                                        '{channel_name}',
                                        '{content_title}',
                                        '{content_published}',
                                        '{content_updated}',
                                        '{record_timestamp}'
                                    )"""))
        
    return

def initialize_scrape_task(video_id):
    #Get current time minus 10 seconds to prioritize the new task in the queue
    current_time = datetime.utcnow()
    initial_run_trigger = current_time - timedelta(seconds=10)

    #Write task in tasks table
    with engine.connect() as connection:
        connection.execute(f"INSERT INTO video_scrape_tasks (video_id, scheduled_execution, prev_schedule_index, task_status, video_lifecycle_status) VALUES ('{video_id}', '{initial_run_trigger}', -1, 'Scheduled', 'In Progress')")
    return

def initialize_subscriptions(channel_list):
  for channel_id in channel_list:
    post_data = {
    "hub.callback": "http://ec2-18-117-130-175.us-east-2.compute.amazonaws.com:5000/feed",
    "hub.mode": "subscribe",
    "hub.topic":f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}",
    "hub.lease_seconds": 864000
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post('https://pubsubhubbub.appspot.com/', headers=headers, data =post_data)

def read_channel_list():
  with open('./channel_targets.txt') as handle:
      lines = handle.readlines()
      channel_ids = [line[:-1] for line in lines]
      return channel_ids

@app.route("/", methods=["GET"])
def index():
    return "Hello World"

@app.route("/feed", methods=["GET", "POST"])
def feed():

    if(request.method == 'GET'):
      # logging.info("------ GET REQUEST -------")
      # logging.info(request.args)
      # logging.info(request.data)

      xml_dict = request.args

      topic = xml_dict.get('hub.topic')
      lease_seconds = xml_dict.get('hub.lease_seconds')
      challenge = xml_dict.get("hub.challenge")

      channel_id = topic.split("channel_id=")[1]
      subscriptions[channel_id] = datetime.utcnow() + timedelta(seconds=int(lease_seconds))
      logging.info(f"Current Subscriptions: {subscriptions}")

      # YT will send a challenge from time to time to confirm the server is alive.
      return str(challenge), 202

    elif (request.method == "POST"):
        try:
            # Parse the XML from the POST request into a dict.
            xml_dict = xmltodict.parse(request.data)
            logging.info(json.dumps(xml_dict, indent=2))

            write_video_notification(xml_dict["feed"])
            initialize_scrape_task(xml_dict["feed"].get("entry", {}).get("yt:videoId"))

        except (ExpatError, LookupError, KeyError):
            # request.data contains malformed XML or no XML at all, return FORBIDDEN.
            return "", 403

    # Everything is good, return NO CONTENT.
    return "", 204

@app.route("/refresh_subscriptions", methods=["GET"])
def refresh_subscriptions():
  channel_list = read_channel_list()
  initialize_subscriptions(channel_list)

  return "subscriptions refreshed", 202

xml_dict = {"feed": {
    "@xmlns:yt": "http://www.youtube.com/xml/schemas/2015",
    "@xmlns": "http://www.w3.org/2005/Atom",
    "link": [
      {
        "@rel": "hub",
        "@href": "https://pubsubhubbub.appspot.com"
      },
      {
        "@rel": "self",
        "@href": "https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCfCwtlMHu67y6zuJA10c_wQ"
      }
    ],
    "title": "YouTube video feed",
    "updated": "2022-06-09T01:00:11.829270127+00:00",
    "entry": {
      "id": "yt:video:XCDnduzy1jU",
      "yt:videoId": "XCDnduzy1jU",
      "yt:channelId": "UCfCwtlMHu67y6zuJA10c_wQ",
      "title": "pubsub video noitification test 8",
      "link": {
        "@rel": "alternate",
        "@href": "https://www.youtube.com/watch?v=XCDnduzy1jU"
      },
      "author": {
        "name": "KiranG",
        "uri": "https://www.youtube.com/channel/UCfCwtlMHu67y6zuJA10c_wQ"
      },
      "published": "2022-06-09T00:55:39+00:00",
      "updated": "2022-06-09T01:00:11.829270127+00:00"
    }
  }}

def post_test(data):
    write_video_notification(data["feed"])
    initialize_scrape_task(data["feed"].get("entry", {}).get("yt:videoId"))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)