#This file defines api functions and their behavior
from datetime import datetime
from http.client import HTTPResponse
import json
from xmlrpc.client import boolean
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from metricsapp.serializers import LiveStreamsSerializer, VideoLifecycleSerializer, VideoLifecycleChannelsSerializer, LiveStreamChannelSerializer
from metricsapp.models import LiveStreams, VideoLifecycle, LiveStreamChannel
import logging;
import pandas as pd
import datetime
import time
from itertools import groupby


logging.basicConfig(filename='django_views.log', level=logging.DEBUG)
logging.info("Logging initialized")

def get_daily_hours_streamed(df):

    utc_offset = time.localtime().tm_gmtoff / (60 * 60)
    df = df.set_index(df["log_time"].dt.tz_localize("UTC").dt.tz_convert("US/Pacific"))

    is_live_markers = list(zip(df.is_live, df.index))
    grouped = [list(g) for k,g in groupby(is_live_markers, lambda x: x[0])]
    logging.info("GROUPED")
    indices = [(m[0][0], min(m)[1], max(m)[1])for m in grouped]
    logging.info("DAILY HOURS INDICES")
    logging.info(indices)

    stream_hours = [{"stream_hours": (g[2] - g[1]).total_seconds() / 60 / 60, "start_date": g[1], "end_date": g[2]} if g[0] else {"stream_hours": 0, "start_date": g[1], "end_date": g[2]} for g in indices]
    hours_df = pd.DataFrame(stream_hours)

    last_date = hours_df.iloc[-1]["end_date"]
    hours_df.loc[len(hours_df.index)] = {"stream_hours": 0, "start_date": last_date,"end_date": last_date}

    hours_df = hours_df.set_index('start_date')
    logging.info(hours_df.tail(10))


    df_aggreagtes = pd.DataFrame()
    df_aggreagtes["streamed_hours"] = hours_df.resample("1D")["stream_hours"].sum()
    logging.info(df_aggreagtes.tail(10))

    # logging.info("AFTER AGG")
    # logging.info(df_aggreagtes.head(5))
    # df_aggreagtes = df_aggreagtes.reset_index()
    # df_aggreagtes["date"] = df_aggreagtes["log_time"].dt
    df_aggreagtes["utc_datetime"] = df_aggreagtes.index
    # logging.info(df_aggreagtes.dtypes)
    # logging.info(df_aggreagtes.head())

    return df_aggreagtes

def get_stream_aggregates(df):
    df["log_time"] = df["log_time"].dt.tz_localize("UTC").dt.tz_convert("US/Pacific")
    df = df.sort_values("log_time")

    is_live_markers = list(zip(df.is_live, df.index))
    grouped = [list(g) for k,g in groupby(is_live_markers, lambda x: x[0]) if k]
    indices = [(min(m)[1], max(m)[1])for m in grouped]
    
    # logging.info(f"stream start and stop indices: {indices}")

    aggs = []
    for stream_start_index, stream_end_index in indices:
        stream = {}
        stream_df = df.loc[stream_start_index:stream_end_index]
        stream['start'] = stream_df.iloc[0]['log_time']
        stream['end'] = stream_df.iloc[-1]['log_time']
        stream['hours'] = (stream_df.iloc[-1]['log_time'] - stream_df.iloc[0]['log_time']).total_seconds() / 60 / 60
        stream['title'] = stream_df.iloc[0]['stream_title']
        stream['thumbnail_url'] = stream_df.iloc[0]['thumbnail_url']
        stream['video_id'] = stream_df.iloc[0]['video_id']

        stream["avg_viewers"] = stream_df.concurrent_viewers.mean()
        stream["min_viewers"] = stream_df.concurrent_viewers.min()
        stream["max_viewers"] = stream_df.concurrent_viewers.max()

        for key, value in stream.items():
            if(pd.isna(value)):
                stream[key] = None

        aggs.append(stream)

    aggs = pd.DataFrame(aggs)
    
    logging.info(aggs.head())
    return aggs

@api_view(['GET'])
def is_live(request):
    channel_id = request.query_params["channel_id"]
    
    obj = LiveStreams.objects.filter(channel_id=channel_id).latest('log_time')

    logging.info(f"is_live request for {channel_id} returned {obj}")
    ser = LiveStreamsSerializer(obj)
    logging.info(f"serialized data is {ser}")
    return Response(ser.data) 

@api_view(['GET'])
def stream_table(request):
    logging.info("Stream table request")
    channel_id = request.query_params["channel_id"]
    min_date = request.query_params["min_date_inclusive"]
    max_date = request.query_params["max_date_exclusive"]
    query = LiveStreams.objects.filter(
        channel_id = channel_id
    ).filter(
        log_time__gte = datetime.datetime.strptime(min_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    ).filter(
        log_time__lt = datetime.datetime.strptime(max_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    )
    df = pd.DataFrame.from_records(query.values())
    if df.empty:
        return JsonResponse({}, safe=False)

    aggs = get_stream_aggregates(df)

    logging.info("POST NAN PROCESSING: ")
    logging.info(aggs)

    data = aggs.to_dict('records')
    # data = json.loads(aggs.to_json(date_format="iso"))
    return JsonResponse(data=data, safe=False)

@api_view(["GET"])
def all_livestreams(request):
    logging.info("all livestreams request made with data: ")
    logging.info(request.query_params)
    #These dates come in in GMT 
    min_date = request.query_params["min_date_inclusive"]
    max_date = request.query_params["max_date_exclusive"]
    channel_id = request.query_params["channel_id"]

    logging.info("QUERY PARAMS MIN DATE:")
    logging.info(min_date)
    logging.info("QUERY PARAMS MAX DATE:")
    logging.info(max_date)

    # query = Livestreams.objects.all().using("mogul_metrics")
    query = LiveStreams.objects.filter(
        channel_id = channel_id
    ).filter(   
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

    for key, value in topline_metrics.items():
            if(pd.isna(value)):
                topline_metrics[key] = None

    live_data = json.loads(dhs_df.to_json(date_format="iso"))["streamed_hours"]
    json_data = {}
    json_data["daily_hours"] = live_data
    json_data["topline"] = topline_metrics
    logging.info(json_data)

    return JsonResponse(json_data, safe=False)

@api_view(["GET"])
def lifecycle_channels(request):
    return

@api_view(["GET"])
def all_stream_channels(request):
    obj = LiveStreamChannel.objects.all()

    df = pd.DataFrame.from_records(obj.values())
    df = df.sort_values(by="log_time").drop_duplicates(subset=["channel_id"], keep="last")
    logging.info(df.head())

    data = json.loads(df.to_json(orient='records', date_format="iso"))

    return JsonResponse(data, safe=False)


    return Response(ser.data) 

@api_view(["GET"])
def streamer_info(request):
    channel_id = request.query_params["channel_id"]

    qs = LiveStreamChannel.objects.filter(
        channel_id = channel_id
    ).order_by('-log_time')[0]

    ser = LiveStreamChannelSerializer(qs)

    return Response(ser.data)

@api_view(["GET"])
def video_lifecycle(request):
    logging.info("video lifecycle request!")
    channel_id = request.query_params["channel_id"]
    min_date = request.query_params["min_date_inclusive"]
    max_date = request.query_params["max_date_exclusive"]

    logging.info(f"Retrieving video view data for videos uploaded between {min_date} and {max_date}")

    import time
    start = time.perf_counter()

    query = VideoLifecycle.objects.filter(
        channel_id = channel_id
    ).filter(
        date_uploaded__gte = datetime.datetime.strptime(min_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    ).filter(
        date_uploaded__lt = datetime.datetime.strptime(max_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    )

    df = pd.DataFrame.from_records(query.values())
    if(df.empty):
        return JsonResponse({}, safe=False)

    df = df.sort_values(by=['record_timestamp'])

    logging.info(df.shape)

    logging.info(f"queried db for {df.shape[0]} rows in {time.perf_counter() - start} seconds")

    video_ids = set(df["video_id"].to_list())
    vid_map = {}
    for id in video_ids:
        vid_map[id] = df[df["video_id"] == id].iloc[0]["date_uploaded"]


    def calc_timedetlas(row):
        return pd.Timedelta(row["record_timestamp"] - vid_map[row["video_id"]], unit='seconds').total_seconds() / 60 / 60

    start = time.perf_counter()

    df["time_delta"] = df.apply(calc_timedetlas, axis=1)

    logging.info(f"Computed time deltas for {df.shape[0]} rows in {time.perf_counter() - start} seconds")

    df = df[["video_id", "time_delta", "views", "date_uploaded", "video_title"]]

    graph_data = df.to_dict('records')

    # logging.info(graph_data)
    # logging.info(df.head())

    return JsonResponse(graph_data, safe=False)