from youtube import YouTubeAPI
import os 
import pytest

def test_get_video_views():
    youtube = YouTubeAPI(os.environ.get("YOUTUBE_API_KEY"))
    views = youtube.get_video_views("i2tQH0lHJXs")
    print(views)
    assert(isinstance(views, int))