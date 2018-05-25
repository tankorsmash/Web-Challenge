import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'
import {
    Collapse, Media, Navbar, NavbarToggler, NavbarBrand, Nav, NavItem,
    NavLink, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem
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
                        <img src="https://discourse-cdn-sjc1.com/business5/uploads/gamedev/optimized/1X/2d1f1721ff9a04b33e75ce2e606e124626104249_1_690x149.png"/>
                    </NavbarBrand>
                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} navbar>
                        <Nav className="ml-auto" navbar>
                        </Nav>
                    </Collapse>
                </Navbar>
            </div>
        );
    }
};

class App extends Component {
    state = {
        chartData: {
            date_labels: [],
            average_axis: [],
            count_axis: [],
        },
    }

    async updateData() {
        const res = await fetch("/ratings")
        const json = await res.json()
        this.setState({
            chartData: json.chart_data
        })
    }

    async componentDidMount() {
        this.updateData();
    }

    render() {
        let rawChartData = this.state.chartData;

        return (
            <div className="">
                <GamedevTvNavbar/>
                <div className="container">
                    <h3>Ratings over time</h3>
                    <RatingChart dateLabels={rawChartData.date_labels} averageAxis={rawChartData.average_axis} countAxis={rawChartData.count_axis}  />
                    <div>
                    </div>
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
