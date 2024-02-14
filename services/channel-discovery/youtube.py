import os
import logging
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from channel import YouTubeChannel

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(self.handler)

    def search_related_videos(self, video_id):
        try:
            response = self.youtube.search().list(
                part="snippet",
                maxResults=10,  # Adjust as needed
                relatedToVideoId=video_id,
                type="video"
            ).execute()

            # Extract and return the list of video resource objects
            video_list = response.get("items", [])
            return video_list

        except HttpError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            return []
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return []
        
    def get_commenters_for_video(self, video_id, pagination_token):
        commenting_accounts = []
        try:
            comments_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=50,
                pageToken=pagination_token
            ).execute()


            # Iterate over the comments and extract commenting accounts
            print(f'found {len(comments_response.get("items"))} comment threads')
            for comment_thread in comments_response.get('items', []):
                snippet = comment_thread.get('snippet', {})
                top_level_comment = snippet.get('topLevelComment', {})
                commenter_id = top_level_comment.get('snippet', {}).get('authorChannelId').get('value')
                if commenter_id:
                    commenting_accounts.append(commenter_id)

                replies = comment_thread.get('replies', [])
                if len(replies) > 0:
                    print(f'found {len(replies)} replies within thread')
                for reply in replies:
                    commenter_id = reply.get('authorChannelId').get('value')
                    commenting_accounts.append(commenter_id)

            next_page_token = comments_response.get('nextPageToken')
            print(next_page_token)
            return commenting_accounts, next_page_token

        except HttpError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            return [], None
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return [], None
        
    def get_account_subscriptions(self, channel_id, subscriber_cutoff, max_results=50):
        subscribed_channels = []
        next_page_token = None
        
        try:
            while True:
                subscriptions_response = self.youtube.subscriptions().list(
                    part="snippet,contentDetails",
                    channelId=channel_id,
                    maxResults=max_results,
                    pageToken=next_page_token
                ).execute()

                # Iterate over the subscriptions and extract channel titles
                for subscription in subscriptions_response.get('items', []):
                    channel_title = subscription['snippet']['title']
                    subscribed_channel_id = subscription['snippet']['resourceId']['channelId']
                    subscriber_count = self.get_channel_subscriber_count(subscribed_channel_id)

                    if subscriber_count < subscriber_cutoff:
                        continue

                    subscribed_channel = YouTubeChannel(subscribed_channel_id, channel_title, subscriber_count)
                    subscribed_channels.append(subscribed_channel)

                # Check if there are more pages to retrieve
                next_page_token = subscriptions_response.get('nextPageToken')
                if not next_page_token:
                    break  # Exit loop if there are no more pages

            return subscribed_channels
        
        except HttpError as e:
            # Check if the error is due to subscription privacy
            if e.resp.status == 403:
                print("Subscription list is not public.")
                return None
            else:
                print('An HTTP error occurred:', e)
                return None

    def get_channel_subscriber_count(self, channel_id):
        try:
            channel_data = self.youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()

            # Extract subscriber count if available
            channel_data_items = channel_data.get('items', [])
            channel_data_entry = channel_data_items[0]
            channel_stats = channel_data_entry.get('statistics', {})
            sub_count = channel_stats.get('subscriberCount')
            sub_count = int(sub_count)
            return sub_count
    
        except HttpError as e:
            print('An HTTP error occurred:', e)
            return None