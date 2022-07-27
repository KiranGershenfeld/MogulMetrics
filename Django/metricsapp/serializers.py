from django.contrib.auth.models import User, Group
from rest_framework import serializers
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