from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import datetime
from hours_streamed import calc_weekly_hours, calc_topline_weekly_metrics

app = Flask(__name__)

@app.route('/')
def weekly_hours():
    today = datetime.datetime.today()
    week_start = datetime.datetime.strftime(today - datetime.timedelta(days=6), '%Y-%m-%d')
    week_end = datetime.datetime.strftime(today, '%Y-%m-%d')
    print(week_start, week_end)
    df = calc_weekly_hours(week_start, week_end)
    fig = px.bar(df, x="Day of Week", y="Hours Streamed", color="Hours Streamed", custom_data=['Hours Streamed'])

    fig.update_traces(marker_color='#7fd4cf') 
    fig.update_layout(
       { "plot_bgcolor": "rgba(0,0,0,0)",
        "paper_bgcolor": "rgba(0,0,0,0)"}
    )
    fig.update_traces(
        hovertemplate="<br>".join(["Hours Streamed: %{customdata[0]}"])
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    metrics = calc_topline_weekly_metrics(df)

    return render_template('page_hours_streamed.html', graphJSON=graphJSON, metrics=metrics)

if __name__ == "__main__":
    app.run(debug=True)