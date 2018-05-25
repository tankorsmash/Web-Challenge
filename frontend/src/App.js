import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'

import RatingChart from './components/RatingChart';

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
            <div className="container">
                <h3> Hourly average </h3>
                <RatingChart dateLabels={rawChartData.date_labels} averageAxis={rawChartData.average_axis} countAxis={rawChartData.count_axis}  />
                <div>
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
