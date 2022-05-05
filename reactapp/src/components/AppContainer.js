import React from 'react';
import axios from 'axios';
import '../css/styles.css'
import CalendarD3 from './CalendarD3';
import * as moment from "moment"

import { Navbar, Nav, NavItem, NavDropdown, MenuItem, Container } from 'react-bootstrap';
import Select from 'react-select'


export default class AppContainer extends React.Component {
    state = {
        data: [],
        dimensions: {
          "height": 700,
          "width": 500,
          "margin": {
            "left": 0,
            "right": 0,
            "top": 10,
            "bottom": 10
          }
        },
        month: ""
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
              for (const [iso_string, hours] of Object.entries(res.data)) {
                data.push({"date": moment(iso_string), "streamed_hours": hours})
              }
              console.log(data)
              this.setState({data: data});
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
          <div className="calendar-section">
            <div className="month-dropdown">
              <Dropdown>
                <Dropdown.Toggle variant="success" id="dropdown-basic">
                  Month
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  <Dropdown.Item href="#/action-1">May 2022</Dropdown.Item>
                  <Dropdown.Item href="#/action-2">April 2022</Dropdown.Item>
                  <Dropdown.Item href="#/action-3">March 2022</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </div>
            <div className="chart-container" id="chart-container">
                <CalendarD3 data={this.state.data} month={this.state.month} year={2022} dimensions={this.state.dimensions} />
            </div>
          </div>
        </div>
      );
    }
  }