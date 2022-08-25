import time
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError
from sqlalchemy import create_engine
from sqlalchemy import text, Table, MetaData
#delete t1 from video_scrape_tasks t1 join row_ranked t2 on t1.video_id = t2.video_id and t2.

import os
from dotenv import load_dotenv
import googleapiclient.discovery
from sqlalchemy.exc import OperationalError

class ScrapeManager():

    def __init__(self, engine, schedule, youtube_api_key):
        self.engine = engine
        self.metadata_obj = MetaData()

        self.schedule = schedule
        self.queue = []

        api_service_name = "youtube"
        api_version = "v3"
        self.youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api_key)

    def attempt_request(self, request, sleep_timeout):
        try:
            response = request.execute()
        except HTTPError as e:
            print(f"YouTube API request returned {e}. Sleeping for {sleep_timeout} seconds...")
            time.sleep(sleep_timeout)
            response = self.attempt_request(request, sleep_timeout * 2)
        return response

    def run(self):
        while True:
            try: 
                print("Looking for tasks")
                #Look for new tasks
                with self.engine.connect() as conn:
                    query = conn.execute(f"SELECT * FROM video_scrape_tasks WHERE scheduled_execution < '{datetime.utcnow()}' AND task_status='Scheduled' AND video_lifecycle_status='In Progress'")
                    for row in query:
                        task_data = row._asdict()
                        self.queue.append(task_data)

                print(f"Found {len(self.queue)} tasks")
                #Perform tasks
                for task in self.queue:
                    video_details = self.get_youtube_video_details(task["video_id"])
                    if(video_details):
                        self.write_view_record(video_details)
                        self.write_new_task(task)
                    elif (video_details == -1):
                        continue
                    else:
                        self.write_task_completion(task, early_end=True)
                    
                #Wait for a minute
                self.queue = []
                time.sleep(20)
            except OperationalError as e:
                print("SQL OperationalError, sleeping for 60 seconds and retrying")
                time.sleep(60)
                continue

    def write_new_task(self, previous_task):
        with self.engine.connect() as conn:
            
            #Previous task information
            video_id = previous_task["video_id"]
            prev_schedule_index = previous_task["prev_schedule_index"]
            prev_task_status = previous_task["task_status"]
            #New task information
            next_task_index = prev_schedule_index + 1

            if(len(self.schedule) <= next_task_index):
                self.write_task_completion(previous_task)
            else:
                #Update status of previous task
                conn.execute(f"UPDATE video_scrape_tasks SET task_status='completed' WHERE video_id='{video_id}' AND prev_schedule_index={prev_schedule_index} AND task_status='{prev_task_status}'")

                next_wait_time = self.schedule[next_task_index]
                print(f"Next task scheduled in {next_wait_time} minutes")
                scheduled_execution_time = datetime.utcnow() + timedelta(minutes=next_wait_time)
                task_status = "Scheduled"
                video_lifecycle_status = "In Progress"

                #Insert new scheduled task
                conn.execute(f"INSERT INTO video_scrape_tasks (video_id, scheduled_execution, prev_schedule_index, task_status, video_lifecycle_status) VALUES ('{video_id}', '{scheduled_execution_time}', {next_task_index}, '{task_status}', '{video_lifecycle_status}')")

    def write_task_completion(self, previous_task, early_end=False):
        with self.engine.connect() as conn:
            #Previous task information
            video_id = previous_task["video_id"]
            prev_schedule_index = previous_task["prev_schedule_index"]
            prev_task_status = previous_task["task_status"]

            #Update status of previous task
            conn.execute(f"UPDATE video_scrape_tasks SET task_status='completed' WHERE video_id='{video_id}' AND prev_schedule_index={prev_schedule_index} AND task_status='{prev_task_status}'")

            #New task information
            next_task_index = prev_schedule_index + 1
            next_wait_time = None
            scheduled_execution_time = None
            task_status = "Video No Longer Available"
            video_lifecycle_status = "Complete"

            #Insert new record to mark video scrape as completed
            conn.execute(f"INSERT INTO video_scrape_tasks (video_id, prev_schedule_index, task_status, video_lifecycle_status) VALUES ('{video_id}', {next_task_index}, '{task_status}', '{video_lifecycle_status}')")

    def write_view_record(self, view_record):
        vvl_table = Table('video_view_lifecycle', self.metadata_obj, autoload_with=self.engine)

        video_id = view_record.get("id")
        video_title = view_record.get("snippet", {}).get("title")
        channel_id = view_record.get("snippet", {}).get("channelId")
        channel_name = view_record.get("snippet", {}).get("channelTitle")
        views = view_record.get("statistics", {}).get("viewCount")
        likes = view_record.get("statistics", {}).get("likeCount")
        favorites = view_record.get("statistics", {}).get("favoriteCount")
        comments = view_record.get("statistics", {}).get("commentCount")
        dislikes = view_record.get("statistics", {}).get("dislikeCount", -1)
        video_duration = view_record.get("contentDetails", {}).get("duration")
        thumbnail_url = view_record.get("snippet", {}).get("thumbnails", {}).get("default",  {}).get("url", "")
        date_uploaded = view_record.get("snippet", {}).get("publishedAt")
        record_timestamp = datetime.utcnow()

        stmt = vvl_table.insert().values(video_id=video_id, video_title=video_title, channel_id=channel_id, channel_name=channel_name, views=views, likes=likes, favorites=favorites, comment_count=comments, dislikes=dislikes, video_duration=video_duration, thumbnail_url=thumbnail_url, date_uploaded=date_uploaded, record_timestamp=record_timestamp)

        with self.engine.connect() as conn:
            res = conn.execute(stmt)
            print(f"Wrote Record View For Video {video_id}")

        
        return

    def get_youtube_video_details(self, video_id):
        #print(f"ATTEMPT FOR VID: {video_id}")
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        #print(f"YouTube API request generated")
        response = self.attempt_request(request, 60)
        #response = request.execute()
        print(video_id)
        print(f"YouTube API response: {response}")

        response = response.get("items", [None])

        if (len(response) == 0):
            return None
        else: 
            if(response[0] == None):
                print("Items not found in API response")
                return -1
            return response[0]
    

def read_schedule():
    with open('./schedule.txt') as handle:
        lines = handle.readlines()
        wait_times = [float(line[:-1]) for line in lines]
        return wait_times

if __name__ == "__main__":
    load_dotenv()

    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    hostname = os.environ.get("DB_HOST")
    database_name = os.environ.get("DB_NAME")
    port = os.environ.get("DB_PORT")
    cluster = os.environ.get("DB_CLUSTER")
    youtube_api_key = os.environ.get("YOUTUBE_API_KEY")

    engine = create_engine(f'cockroachdb://{user}:{password}@{hostname}:{port}/mogul_metrics?sslmode=require&options=--cluster={cluster}')
    schedule = read_schedule()
    
    manager = ScrapeManager(engine, schedule, youtube_api_key)
    manager.run()
