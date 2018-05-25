import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'
import {
    NavbarBrand, Navbar, Collapse
} from 'reactstrap';
import './App.css';

import RatingChart from './components/RatingChart';

class GamedevTvNavbar extends Component {
    render() {
        return (
            <div>
                <Navbar id="gamedevtv-navbar" color="light" light expand="md">
                    <NavbarBrand href="/">
                        <img alt="GamedevTV logo" src="https://discourse-cdn-sjc1.com/business5/uploads/gamedev/optimized/1X/2d1f1721ff9a04b33e75ce2e606e124626104249_1_690x149.png"/>
                    </NavbarBrand>
                    <Collapse navbar/>
                </Navbar>
            </div>
        );
    }
};

class App extends Component {
    render() {
        return (
            <div>
                <GamedevTvNavbar/>
                <div className="container">
                    <h3>Complete C# Unity Developer 3D - Learn to Code Making Games</h3>
                    <RatingChart/>
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
