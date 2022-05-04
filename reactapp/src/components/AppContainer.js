import React from 'react';
import axios from 'axios';
import '../css/styles.css'
import CalendarD3 from './CalendarD3';


export default class AppContainer extends React.Component {
    state = {
        data: [
          {"x": 0, "y": 0},
          {"x": 1, "y": 1},
          {"x": 2, "y": 2},
          {"x": 3, "y": 3},
          {"x": 4, "y": 4},
          {"x": 5, "y": 5}
        ],
        dimensions: {
          "height": 500,
          "width": 500,
          "margin": {
            "left": 30,
            "right": 10,
            "top": 10,
            "bottom": 10
          }
        }
    };
    
    componentDidMount() {
        console.log("Mounting")
        // axios.get('api/all_livestreams')
        //     .then(res => {
        //         this.setState({data: res.data});
        //     });
        console.log("AppContainer component data, dimensions:")
        console.log(this.state.data)
        console.log(this.state.dimensions)
    }
  
    render() {
      return (
        <div className="chart-container">
            <CalendarD3 data={this.state.data} dimensions={this.state.dimensions} />
        </div>
      );
    }
  }