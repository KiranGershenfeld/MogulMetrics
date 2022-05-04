import React from 'react';
import axios from 'axios';
import '../css/styles.css'


export default class TaggingApp extends React.Component {
    state = {
        data: {}
      };
    
      componentDidMount() {
        console.log("Mounting")
        axios.get('api/all_livestreams')
            .then(res => {
                this.setState({data: res.data});
            });
        
    }
  
    render() {
      return (
        <div className="testing">
            <span>{JSON.stringify(this.state.data)}</span>
        </div>
      );
    }
  }