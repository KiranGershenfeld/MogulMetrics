import os
import logging
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from channel import YouTubeChannel
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

            # Check for HTTP errors
            response.raise_for_status()

            # Parse JSON response safely
            data = response.json()

            # Check for unexpected JSON structure
            if 'items' not in data or len(data['items']) == 0 or 'statistics' not in data['items'][0]:
                raise json.JSONDecodeError("Unexpected JSON structure")

            # Extract video view count
            view_count = data['items'][0]['statistics']['viewCount']

            view_count = int(view_count)

            return view_count

    def get_video_views_scrape(self, video_id):
        raise NotImplemented()
    
    def get_video_views(self, video_id, method='api'):
        if(method == 'api'):
            self.get_video_views_api(video_id)
        elif(method == 'scrape'):
            self.get_video_views_scrape(video_id)
