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
import time

logging.basicConfig(filename='django_views.log', level=logging.DEBUG)
logging.info("Logging initialized")

def get_daily_hours_streamed(df):

    utc_offset = time.localtime().tm_gmtoff / (60 * 60)
    df = df.set_index(df["log_time"].dt.tz_localize("UTC").dt.tz_convert("US/Pacific"))
    
    df_aggreagtes = pd.DataFrame()
    df_aggreagtes["streamed_hours"] = df.resample("1D")["is_live"].apply(lambda x: (x == True).sum() / 6)
    logging.info("AFTER AGG")
    # logging.info(df_aggreagtes.head(5))
    # df_aggreagtes = df_aggreagtes.reset_index()
    # df_aggreagtes["date"] = df_aggreagtes["log_time"].dt
    df_aggreagtes["utc_datetime"] = df_aggreagtes.index
    # logging.info(df_aggreagtes.dtypes)
    # logging.info(df_aggreagtes.head())

    return df_aggreagtes

@api_view(["GET"])
def all_livestreams(request):
    logging.info("all livestreams request made with data: ")
    logging.info(request.query_params)
    #These dates come in in GMT 
    min_date = request.query_params["min_date_inclusive"]
    max_date = request.query_params["max_date_exclusive"]
    logging.info("QUERY PARAMS MIN DATE:")
    logging.info(min_date)
    logging.info("QUERY PARAMS MAX DATE:")
    logging.info(max_date)

    # query = Livestreams.objects.all().using("mogul_metrics")
    query = LiveStreams.objects.filter(
        log_time__gte = datetime.datetime.strptime(min_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    ).filter(
        log_time__lt = datetime.datetime.strptime(max_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    )

    df = pd.DataFrame.from_records(query.values())
    if(df.empty):
        return JsonResponse({}, safe=False)

    dhs_df = get_daily_hours_streamed(df)
    topline_metrics = {}
    topline_metrics["monthly_hours_streamed"] = dhs_df["streamed_hours"].sum()
    topline_metrics["average_daily_hours"] = dhs_df["streamed_hours"].mean()
    topline_metrics["average_stream_length"] = dhs_df[dhs_df["streamed_hours"] != 0]["streamed_hours"].mean()
    live_data = json.loads(dhs_df.to_json(date_format="iso"))["streamed_hours"]
    json_data = {}
    json_data["daily_hours"] = live_data
    json_data["topline"] = topline_metrics
    logging.info(json_data)

    return JsonResponse(json_data, safe=False)

