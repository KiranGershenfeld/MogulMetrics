import React from 'react';
import axios from 'axios';
import { CSVLink, CSVDownload } from "react-csv";
import numeral from 'numeral'

import '../css/styles.css'
import CalendarD3 from './CalendarD3';
import * as moment from "moment"
import {config} from '../constants'

import MogulNavBar from './Navbar'
import Select from 'react-select'
import Card from 'react-bootstrap/Card';
import ProfilePhoto from '../static/ludwigprofile.jpg' // relative path to image 
import StreamsTable from './StreamsTable';

const API_URL = config.url.API_URL

const options = [
  { value: 0, label: 'January' },
  { value: 1, label: 'February' },
  { value: 2, label: 'March' },
  { value: 3, label: 'April' },
  { value: 4, label: 'May' },
  { value: 5, label: 'June' },
  { value: 6, label: 'July' },
  { value: 7, label: 'August' },
  { value: 8, label: 'September' },
  { value: 9, label: 'October' },
  { value: 10, label: 'November' },
  { value: 11, label: 'December' },
]
const year = 2022
const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function getMonthDateRange(year, month) {
  var moment = require('moment-timezone');

  // month in moment is 0 based, so 9 is actually october, subtract 1 to compensate
  // array is 'year', 'month', 'day', etc
  var startDate = moment.tz([year, month], 'America/Los_Angeles');
  // Start date is in computer local time

  // Clone the value before .endOf()
  var endDate = moment(startDate).endOf('month');

  // make sure to call toDate() for plain JavaScript date type
  return { start: startDate, end: endDate };
}

export default class AppContainer extends React.Component {
    constructor(props){
      super(props);
      this.set_selected_month=this.set_selected_month.bind(this);
    } 

    state = {
        data: [],
        dimensions: {
          "height": 600,
          "width": 500,
          "margin": {
            "left": 0,
            "right": 0,
            "top": 10,
            "bottom": 10
          }
        },
        month: "",
        topline_metrics: {},
        streamsTableData: [],
        csvData: [],
        channel_info: {},
    };

    set_selected_month(channel_id, month_index, year)
    {      
      var dateRange = getMonthDateRange(year, month_index)

      axios.get(`${API_URL}/api/all_livestreams`, { 
          params: {
            channel_id : channel_id,
            min_date_inclusive: dateRange['start'].toISOString(),
            max_date_exclusive: dateRange['end'].toISOString(),
          }
        },{
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then(res => {
            var data = []
            if(Object.keys(res.data).length === 0)
            {
              this.setState({data: {}});
              this.setState({topline_metrics: {}})
            }
            if(!("daily_hours" in res.data))
            {
              this.setState({data: {}});
            }
            if(!("topline" in res.data))
            {
              this.setState({topline_metrics: {}});
            }

            for (const [iso_string, hours] of Object.entries(res.data["daily_hours"])) {
               data.push({"date": moment(iso_string), "streamed_hours": hours})
            }
            this.setState({data: data});
            this.setState({topline_metrics: res.data["topline"]})
          });

      this.state.month = (month_index + 1).toString();
      if(this.state.month.length == 1)
      {
        this.state.month = "0"+ this.state.month
      }
      this.state.dimensions.width = document.getElementById("chart-container").offsetWidth

    }
    
    componentDidMount() {
      var urlParams = new URLSearchParams(window.location.search)
      var channel_id = urlParams.get('channel_id')

      axios.get(`${API_URL}/api/streamer_info`, { 
        params: {
          channel_id: channel_id,
        }
      },{
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(res => {
          if(Object.keys(res.data).length === 0)
          {
            this.setState({channel_info: {}});
          }
          else{
            this.setState({channel_info: res.data})
          }
        });

      var month = new Date().getMonth()

      axios.get(`${API_URL}/api/stream_table`, { 
        params: {
          channel_id: channel_id,
          min_date_inclusive: new Date(2022, 7, 30),
          max_date_exclusive: new Date(year, month + 1, 1)
        }
      },{
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(res => {
          if(Object.keys(res.data).length === 0)
          {
            this.setState({streamsTableData: []});
          }
          else{
            this.setState({streamsTableData: res.data})
            this.setState({csvData: res.data})
          }
        });

        this.set_selected_month(channel_id, month, year)

    }

    render() {
      return (
        <div>
          <MogulNavBar />
          {/* <div className='error-message'>
            Working on a fix for the calendar, the data collection is working fine its purely a visual bug. Sorry for the inconvenience!
          </div> */}
          <div className='main-panel-content'>
          <div className='channel-container'>
            <Card className= "channel-card d-flex vertical-center" style={{"marginTop": "10px", "padding": "1px 1px 1px 1px"}}>
              <Card.Body>
                <div style={{"display": "flex", "justifyContent": "center", "alignItems": "center"}}>
                  <img src={this.state.channel_info.thumbnail_url} alt="Profile" style={{"borderRadius": "50%", "width": "15%", "flexGrow": "1"}}></img>
                  <div style={{"flexGrow": "1", "width": "85%", "marginLeft": "15px", "fontSize": "20px", "fontWeight": "450"}}>
                    <div>
                      {this.state.channel_info.channel_name}
                    </div>
                    <div style={{"fontSize": "13px", "color": "grey"}}>
                      {numeral(this.state.channel_info.subscriber_count).format('0.0a')} Subscribers
                    </div>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </div>
          
          <div className="monthly-metrics-section">
            <div className="month-dropdown" style={{"width": "30%", "marginTop": "15px"}}>
              <Select
                options={options}
                defaultValue={{ value: new Date().getMonth(), label: monthNames[new Date().getMonth()]}}
                onChange={(e) => this.set_selected_month(this.state.channel_info.channel_id, e.value, year)}
              />
            </div>
            <div className="topline-container">
              <Card className= "metrics-card" style={{"marginRight": "10px"}}>
                <Card.Body>
                <span className='metrics-title'>Hours Streamed</span>
                <div>
                  <span className='metrics-metric'>
                      {parseFloat(this.state.topline_metrics.monthly_hours_streamed).toFixed(2)}
                  </span>
                </div>
                </Card.Body>
              </Card>
              <Card className= "metrics-card" style={{"marginRight": "10px"}}>
                <Card.Body>
                <span className='metrics-title'>Average Daily Hours</span>
                <div>
                  <span className='metrics-metric'>
                      {parseFloat(this.state.topline_metrics.average_daily_hours).toFixed(2)}
                  </span>
                </div>
                </Card.Body>
              </Card>
              <Card className= "metrics-card" style={{"marginRight": "0px"}}>
                <Card.Body>
                  <span className='metrics-title'>Average Stream Length</span>
                <div>
                  <span className='metrics-metric'>
                      {parseFloat(this.state.topline_metrics.average_stream_length).toFixed(2)}
                  </span>
                </div>
                </Card.Body>
              </Card>
            </div>
            <div className="chart-container" id="chart-container">
                <CalendarD3 data={this.state.data} month={this.state.month} year={2022} dimensions={this.state.dimensions} />
            </div>
          </div>
        </div>
        <div className="streamstable-container">
              <div style={{"height": "10px"}}></div>
              <StreamsTable data={this.state.streamsTableData} channel={this.state.channel_info.channel_name}/>
            </div>
      </div>
      );
    }
  }