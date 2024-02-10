import React from "react";
import {config} from '../constants'

import { css } from "@emotion/css";
import MenuIcon from '../static/menu_icon.png'
import { Link } from "react-router-dom";
import axios from 'axios';
const API_URL = config.url.API_URL

const easeSlow = css`
  transition: all 450ms ease-in-out;
`;

const divider = css`
    margin: auto;
    margin-bottom: 10px;
    margin-top: 10px;
    width: 70%;
    height: 0px !important;
    background-color: white;
    border-top: 1px solid white;
    opacity: 1;
`;

const menuBtn = css`
  position: absolute;
  z-index: 3;
  left: 0px;
  top: 8px;
  cursor: pointer;
  ${easeSlow};
  &.closer {
    transform: rotate(180deg);
    transform-origin: 50% 50%
  }
`;

const menuOverlay = css`
  z-index: 2;
  position: fixed;
  top: 0;
  left: 0;
  background-color: white;
  height: 100vh;
  width: 20vw;
  transform: translateX(-100%);
  transition: all 400ms ease-in-out;
  &.show {
    background-color: #212529;
    transform: translateX(0%); 
  }
  nav {
    padding-top: 60px;
    display: flex;
    flex-direction: column;
    align-items: center;
    a {
      text-align: center;
      height: 100%;
      padding-top: 15px;
      padding-bottom: 15px;
      text-decoration: none;
      color: white;
      cursor: pointer;
      transition: all 150ms ease-in-out;
      &:hover {
        color: #A2E4B8;
      } 
    }
  }
  @media (max-width: 800px) {
    width: 100vw;
  }
`;

class Menu extends React.Component {
  state = {
    isMenuOpen: false,
    channels: [],
  };

  componentDidMount()
  {
    axios.get(`${API_URL}/api/all_stream_channels`, { 
    },{
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        if(Object.keys(res.data).length === 0)
        {
          this.setState({channels: []});
        }
        else{
          this.setState({channels: res.data})
          console.log(`CHANNELS STATE ${this.state.channels}`)
        }
      });
  }

  toggleMenu = () =>
    this.setState(({ isMenuOpen }) => ({ isMenuOpen: !isMenuOpen }));

  render() {
    var channel_links = this.state.channels.map(function(channel)
    {
      return <div style={{'width': '100%', 'textAlign': 'center'}}>
                <Link style={{'fontSize': '1.15em', 'letterSpacing': '0.05rem'}} to={`/main?channel_id=${channel.channel_id}`} onClick={() => { window.location.href(`/main?channel_id=${channel.channel_id}`) }}> {channel.channel_name.toUpperCase()}</Link>
                <hr className={`${divider}`} />
              </div>
    });
  
    const { isMenuOpen } = this.state;
    return (
      <React.Fragment>
        <div
          className={`${menuBtn} ${isMenuOpen ? "closer" : null}`}
          onClick={this.toggleMenu}
        >
        <img src={MenuIcon} alt="menu_icon" style={{"width": "30px", "height": "30px", "margin-left": "10px",  "margin-right": "10px"}}></img>
        
        </div>
        <div className={`${menuOverlay} ${isMenuOpen ? "show" : null}`}>
          <nav>
            {channel_links}
            <Link style={{'paddingTop': '0px', 'fontSize': '1.15em', 'letterSpacing': '0.05rem'}} to={"/about"}>ABOUT</Link>
          </nav>
        </div>
      </React.Fragment>
    );
  }
}

export default Menu;
