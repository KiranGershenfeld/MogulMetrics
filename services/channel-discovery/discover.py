import youtube
import os
from utils import deduplicate_csv
import csv

VIDEO_ID = "1NzLGYRYHJo" 

def crawl(youtube):
    next_page_token = None
    all_commenters = []
    while True:
        commenters, next_page_token = youtube.get_commenters_for_video(VIDEO_ID, next_page_token)
        print(len(commenters))
        all_commenters.extend(commenters)
        print(len(all_commenters))
        if not next_page_token:
            break

    print(f'Found {len(all_commenters)} commenters')

    channels_to_subscribe_to = set()
    for commenter in all_commenters:
        print(commenter)
        subscriptions = youtube.get_account_subscriptions(commenter, 100000)
        if not subscriptions:
            continue

        add_channels_to_csv('./output.csv', subscriptions)

    return channels_to_subscribe_to

def add_channels_to_csv(csv_filepath, channels):
    # Open the CSV file in append mode
    with open(csv_filepath, 'a', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write each channel's data as a row in the CSV file
        for channel in channels:
            channel_id = channel.id
            channel_name = channel.name
            subscriber_count = channel.subscriber_count
            csv_writer.writerow([channel_id, channel_name, subscriber_count])
    
if __name__ == "__main__":
    deduplicate_csv('output.csv')
    # api_key = os.environ.get("YOUTUBE_API_KEY")
    # if not api_key:
    #     exit(1)
    # youtube = youtube.YouTubeAPI(api_key)

    # channels = crawl(youtube)
    
    