#This file defines api functions and their behavior
from datetime import datetime
from http.client import HTTPResponse
import json
from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from metricsapp.serializers import LiveStreamsSerializer
from metricsapp.models import LiveStreams
import logging;
import pandas as pd
import datetime

logging.basicConfig(filename='django_views.log', encoding='utf-8', level=logging.DEBUG)
logging.info("Logging initialized")

def get_daily_hours_streamed(df):
    logging.info(df.head())
    df = df.set_index(df["log_time"])
    # print(df.head())

    df_aggreagtes = pd.DataFrame()
    df_aggreagtes["streamed_hours"] = df.resample("1D")["is_live"].apply(lambda x: (x == True).sum() / 6)
    # df_aggreagtes = df_aggreagtes.reset_index()
    # df_aggreagtes["date"] = df_aggreagtes["log_time"].dt
    df_aggreagtes["utc_datetime"] = df_aggreagtes.index
    logging.info(df_aggreagtes.dtypes)
    logging.info(df_aggreagtes.head())

    return df_aggreagtes

@api_view(["GET"])
def all_livestreams(request):
    logging.info("all livestreams request made with data: ")
    logging.info(request.query_params)
    #These dates come in in GMT 
    min_date = request.query_params["min_date_inclusive"]
    max_date = request.query_params["max_date_exclusive"]
    logging.info(min_date)
    logging.info(max_date)

    # query = Livestreams.objects.all().using("mogul_metrics")
    logging.info("REQUEST MADE")
    query = LiveStreams.objects.filter(
        log_time__gte = datetime.datetime.strptime(min_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    ).filter(
        log_time__lt = datetime.datetime.strptime(max_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    )

    df = pd.DataFrame.from_records(query.values())
    dhs_df = get_daily_hours_streamed(df)
    topline_metrics = {}
    topline_metrics["monthly_hours_streamed"] = dhs_df["streamed_hours"].sum()
    topline_metrics["average_daily_hours"] = dhs_df["streamed_hours"].sum() / len(dhs_df["streamed_hours"])
    topline_metrics["average_stream_length"] = dhs_df[dhs_df["streamed_hours"] != 0]["streamed_hours"].mean()
    live_data = json.loads(dhs_df.to_json(date_format="iso"))["streamed_hours"]
    json_data = {}
    json_data["daily_hours"] = live_data
    json_data["topline"] = topline_metrics
    logging.info(json_data)

    return JsonResponse(json_data, safe=False)

