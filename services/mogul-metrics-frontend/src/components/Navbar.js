import React from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem, Container } from 'react-bootstrap';
import Menu from './Menu'

class MogulNavBar extends React.Component {
  render() {
    return (
      <React.Fragment>
        <div className="nav-bar-container">
            <Navbar className="" bg="dark" expand="lg" variant="dark">
                <Menu />
                <div className="m-auto" style={{"justify-content": "center"}}>
                  <Navbar.Brand href="#home">MOGUL METRICS</Navbar.Brand>
                </div>
            </Navbar>
          </div>
      </React.Fragment>
    );
  }
}

export default MogulNavBar;
