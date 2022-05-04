import pandas as pd
import datetime
from sqlalchemy import create_engine
import os
import cockroachdb.sqlalchemy.dialect
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ['SQLALCHEMY_CONNECTION_URL'])
DB_NAME = "MOGUL_METRICS"

def calc_weekly_hours(week_start, week_end):
    week_start += " 00:00:00"
    week_end += " 00:00:00"

    with engine.begin() as conn:
        conn.execute("USE MOGUL_METRICS")

    df = pd.read_sql(f"SELECT * FROM live_streams WHERE is_live=true AND log_time > '{week_start}' and log_time <= '{week_end}'", engine)
    df = df.set_index(df["log_time"])
    print(df.head())

    week_aggreagtes = pd.DataFrame()
    week_aggreagtes["hour_count"] = df["log_time"].resample("1D").count() / 6
    week_aggreagtes = week_aggreagtes.reset_index()
    week_aggreagtes["day_of_week"] = week_aggreagtes["log_time"].dt.day_name()

    date_cursor = pd.to_datetime(week_start)
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        if day not in week_aggreagtes["day_of_week"].to_list():
            week_aggreagtes.loc[len(week_aggreagtes.index)] = [date_cursor, 0, day]
        date_cursor  = date_cursor + pd.DateOffset(1)

    week_aggreagtes = week_aggreagtes.rename(columns={"log_time": "Date", "hour_count": "Hours Streamed", "day_of_week": "Day of Week"})
    return week_aggreagtes

def calc_topline_weekly_metrics(weekly_aggregates):
    #Calculating total hours streamed this week, avergae daily hours, 
    metrics = {}
    metrics["total_hours_streamed"] = weekly_aggregates["Hours Streamed"].sum()
    metrics["average_daily_hours"] = round(weekly_aggregates["Hours Streamed"].mean(), 2)
    return metrics

if __name__ == "__main__":
    aggs = calc_weekly_hours("2022-02-28", "2022-03-07")
    print(aggs)




#Planned views
"""
Bar chart 
Each x axis increment is a day
Gets more or less smushed based on how many days are picked in a top level range filter

So theres two calendar pickers at the top that affect all views

The point of this is there is a seperate section for videos

3 main pages
Live Stream Metrics
    * User selects two dates
    * See's live hour breakdown and some aggregate metrics across those dates
Video Performance Metrics
    * Channel multiselector
    * Top performers by view delta this week, month
    * Most recent


Outlier Performance
    * Query every video's view count, every day
    * Save a record of each video, its upload date, the current date, and its current viewcount (and channel name, channel id, video thumbnail)
    * Plot each video with days out from upload and view count delta from the previous day 
    * Perform a regression on these points to create an equation that models view decay over time
    * Use that model to predict how many views each video should have gotten in the past day, and rank them by deviation from the prediction.
    * Display video positive and negative outliers
Social Media Metrics
"""