import React from "react";
import { css } from "@emotion/css";
import MenuIcon from '../static/menu_icon.png'
import { Link } from "react-router-dom";

const easeSlow = css`
  transition: all 450ms ease-in-out;
`;

const divider = css`
    margin: 0;
    width: 80%;
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
    isMenuOpen: false
  };

  toggleMenu = () =>
    this.setState(({ isMenuOpen }) => ({ isMenuOpen: !isMenuOpen }));

  render() {
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
            <Link to={"/"}>LIVESTREAM CALENDAR</Link>
            <hr className={`${divider}`} />
            <Link to={"/videolifecycle"}>VIDEO LIFECYCLE</Link>
            <hr className={`${divider}`} />
            <Link to={"/about"}>ABOUT</Link>
          </nav>
        </div>
      </React.Fragment>
    );
  }
}

export default Menu;
