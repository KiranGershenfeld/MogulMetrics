import React from 'react';
import axios from 'axios';
import '../css/styles.css'
import CalendarD3 from './CalendarD3';
import * as moment from "moment"

import { Navbar, Nav, NavItem, NavDropdown, MenuItem, Container } from 'react-bootstrap';
import Select from 'react-select'
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import Card from 'react-bootstrap/Card';

const options = [
  { value: "04", label: 'May' },
  { value: "03", label: 'April' },
  { value: "02", label: 'March' }
]

export default class AppContainer extends React.Component {
    state = {
        data: [],
        dimensions: {
          "height": 800,
          "width": 500,
          "margin": {
            "left": 0,
            "right": 0,
            "top": 10,
            "bottom": 10
          }
        },
        month: "",
        topline_metrics: {}
    };
    
    componentDidMount() {
      var date = new Date()
      var firstDay = new Date(date.getFullYear(), date.getMonth() -1, 1);
      var lastDay = new Date(date.getFullYear(), date.getMonth(), 0);
        axios.get('api/all_livestreams', { 
            params: {
               min_date_inclusive: firstDay.toISOString(),
               max_date_exclusive:  lastDay.toISOString(),
            }
          },{
             headers: {
              'Content-Type': 'application/json'
            }
          })
            .then(res => {
              var data = []
              for (const [iso_string, hours] of Object.entries(res.data["daily_hours"])) {
                data.push({"date": moment(iso_string), "streamed_hours": hours})
              }
              console.log(data)
              this.setState({data: data});
              this.setState({topline_metrics: res.data["topline"]})
            });

      this.state.month = moment().format("MM") 
      this.state.month = "04"
      this.state.dimensions.width = document.getElementById("chart-container").offsetWidth

    }
  
    render() {
      return (
        <div>
          <div className="nav-bar-container">
            <Navbar className="justify-content-center" bg="dark" expand="lg" variant="dark">
                <Navbar.Brand href="#home">MOGUL METRICS</Navbar.Brand>
            </Navbar>
          </div>
          
          <div className="monthly-metrics-section">
            <div className="month-dropdown" style={{"width": "50%", "margin-top": "15px"}}>
              <Select
                options={options}
              />
            </div>
            <div className="topline-container">
              <Card className= "metrics-card" style={{"margin-right": "10px"}}>
                <Card.Body>
                <span className='metrics-title'>Hours Streamed</span>
                <div>
                  <span className='metrics-metric'>
                      {parseFloat(this.state.topline_metrics.monthly_hours_streamed).toFixed(0)}
                  </span>
                </div>
                </Card.Body>
              </Card>
              <Card className= "metrics-card" style={{"margin-right": "10px"}}>
                <Card.Body>
                <span className='metrics-title'>Average Daily Hours</span>
                <div>
                  <span className='metrics-metric'>
                      {parseFloat(this.state.topline_metrics.average_daily_hours).toFixed(2)}
                  </span>
                </div>
                </Card.Body>
              </Card>
              <Card className= "metrics-card" style={{"margin-right": "0px"}}>
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
      );
    }
  }