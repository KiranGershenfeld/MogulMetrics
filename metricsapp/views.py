#This file defines api functions and their behavior
from datetime import datetime
from http.client import HTTPResponse
from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from metricsapp.serializers import LiveStreamsSerializer
from metricsapp.models import LiveStreams
import logging;

def all_livestreams(request):
    # query = Livestreams.objects.all().using("mogul_metrics")
    query = LiveStreams.objects.all()

    serialized_data = LiveStreamsSerializer(query, many=True) #Many because multiple objects need to be serialized
    return JsonResponse(serialized_data.data, safe=False)

