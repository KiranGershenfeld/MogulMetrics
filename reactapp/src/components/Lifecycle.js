import React from 'react';
import axios from 'axios';

import MogulNavBar from './Navbar'
import Select from 'react-select'
import Card from 'react-bootstrap/Card';
import ProfilePhoto from '../static/ludwigprofile.jpg' // relative path to image 
import VideoViewPlot from './VideoViewPlot';

import '../css/styles.css'
import {config} from '../constants'


const API_URL = config.url.API_URL


export default class LifecycleContainer extends React.Component {
  constructor(props){
    super(props);
    this.query_videos=this.query_videos.bind(this);
  } 

  state = {
      data: [],
      dimensions: {
        "height": 400,
        "width": 500,
        "margin": {
          "left": 75,
          "right": 0,
          "top": 0,
          "bottom": 50,
        }
      },
  };

  query_videos(channel_id, start_date, end_date)
  {
    axios.get(`${API_URL}/api/video_lifecycle`, { 
      params: {
        channel_id: channel_id,
        min_date_inclusive: start_date,
        max_date_exclusive:  end_date,
      }
    },{
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        var data = []
        console.log("RECIEVED DATA: ")
        console.log(res.data)
        if(Object.keys(res.data).length === 0)
        {
          this.setState({data: []});
          this.setState({topline_metrics: {}})
        }
        else
        {
          data = res.data
          this.setState({data: data});
        }
      });

  }

  componentDidMount() {
    var currDate = new Date()
    var monthPrevdate = new Date();
    monthPrevdate.setMonth(monthPrevdate.getMonth() - 1);
    console.log(monthPrevdate)
    this.query_videos('UCz6XquIbM5OcfK7r3hQQCXA', monthPrevdate, currDate)
  }

  render() {
    return (
      <div>
        <MogulNavBar />
        <div style={{margin: "auto", marginTop: "25px", width: "30%", textAlign:"center"}}>
            <div >Video View Lifecycle for <span style={{fontWeight: "bold"}}>Ludwin Clips</span></div>
        </div>
        <div style={{margin: "auto", marginTop: "15px", marginBottom: "25px", width: "50%", textAlign:"center"}}>
            <div >This chart shows the view count of videos at a given time after its upload. It demonstrates how the algorithm is recommending videos across their lifecycle</div>
        </div>
        <div className="video-chart-container" id="video-chart-container">
          <VideoViewPlot data={this.state.data} dimensions={this.state.dimensions} />
        </div>
      </div>
    );
  }
}