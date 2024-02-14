import os
import logging
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import json

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(self.handler)

    def get_video_views_api(self, video_id):
            # Make a GET request to the YouTube Data API
            response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            # Check for unexpected JSON structure
            if 'items' not in response or len(response['items']) == 0 or 'statistics' not in response['items'][0]:
                raise json.JSONDecodeError("Unexpected JSON structure")

            # Extract video view count
            view_count = response['items'][0]['statistics']['viewCount']
            view_count = int(view_count)

            return view_count

    def get_video_views_scrape(self, video_id):
        raise NotImplemented()
    
    def get_video_views(self, video_id, method='api'):
        if(method == 'api'):
            return self.get_video_views_api(video_id)
        elif(method == 'scrape'):
            return self.get_video_views_scrape(video_id)

    def most_recent_videos(self, count, channel_id):
        response = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=count,
            order="date"
        ).execute()

        
        videos = []
        try:
            for item in response['items']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_description = item['snippet']['description']
                videos.append({'id': video_id, 'title': video_title, 'description': video_description})
        except KeyError as e:
            raise json.JSONDecodeError(f"Could not parse response for channel id {channel_id}", response, e)
        
        return videos