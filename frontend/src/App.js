import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'
import { Line } from 'react-chartjs-2';

class App extends Component {
    state = {
        chartData: {
            date_labels: [],
            average_axis: [],
            count_axis: [],
        },
    }

    async componentDidMount() {
        const res = await fetch("/ratings")
        const json = await res.json()
        this.setState({
            chartData: json.chart_data
        })
    }

    render() {
        let rawChartData = this.state.chartData;

        const limit = 1000;
        let chartData = {
            labels: rawChartData.date_labels.slice(0, limit),
            datasets: [{
                label: "Averages",
                data: rawChartData.average_axis.slice(0, limit),
                fill: false,
                yAxisID: "y-axis-avg",
            },{
                label: "Total Ratings",
                data: rawChartData.count_axis.slice(0, limit),
                fill: false,
                yAxisID: "y-axis-count",
            }]
        };

        let chartOptions = {
            responsive: true,
            scales: {
                stacked: false,
                yAxes: [{
                    type: "linear",
                    position: "left",
                    display: true,
                    id: "y-axis-avg",
                }, {
                    type: "linear",
                    display: true,
                    position: "right",
                    id: "y-axis-count",

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            },
        };

        return (
            <div className="container">
                <h3> Hourly average </h3>
                <Line  options={chartOptions} data={chartData} />
                <div>
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
