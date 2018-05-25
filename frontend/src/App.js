import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'
import {
    NavbarBrand, Navbar
} from 'reactstrap';
import './App.css';

import RatingChart from './components/RatingChart';

class GamedevTvNavbar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isOpen: false
        };
    }

    toggle = () => {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        return (
            <div>
                <Navbar id="gamedevtv-navbar" color="light" light expand="md">
                    <NavbarBrand href="/">
                        <img alt="GamedevTV logo" src="https://discourse-cdn-sjc1.com/business5/uploads/gamedev/optimized/1X/2d1f1721ff9a04b33e75ce2e606e124626104249_1_690x149.png"/>
                    </NavbarBrand>
                </Navbar>
            </div>
        );
    }
};

class App extends Component {
    render() {
        return (
            <div className="">
                <GamedevTvNavbar/>
                <div className="container">
                    <h3>Ratings over time</h3>
                    <RatingChart/>
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
