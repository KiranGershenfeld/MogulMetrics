from django.contrib.auth.models import User, Group
from rest_framework import serializers
from metricsapp.models import LiveStreamChannel
from metricsapp.models import VideoLifecycle
from metricsapp.models import LiveStreams



class LiveStreamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStreams
        fields = "__all__"


class VideoLifecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLifecycle
        fields = "__all__"

class LiveStreamChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStreamChannel
        fields = "__all__"

class VideoLifecycleChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLifecycle
        fields = ['channel_id', 'channel_name']