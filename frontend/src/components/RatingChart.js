import React from 'react';
// import PropTypes from 'prop-types';

import { Button } from 'reactstrap';
import { Line } from 'react-chartjs-2';

export default class RatingChart extends React.Component {
    state = {
        chartData: {
            date_labels: [],
            average_axis: [],
            count_axis: [],
        },
        refreshButtonText: 'Refresh',
        forceUpdateButtonText: 'Force Update',

    }

    updateData = async () => {
        this.setState({
            refreshButtonText: 'Refreshing...',
            dataButtonsDisabled: true,
        });
        const res = await fetch('/fetch_ratings')
        const json = await res.json()
        this.setState({
            chartData: json.chart_data,
            refreshButtonText: 'Refresh',
            dataButtonsDisabled: false,
        })
    }

    async componentDidMount() {
        this.updateData();
    }

    forceUpdate = async () => {
        this.setState({
            forceUpdateButtonText: 'Forcing update...',
            dataButtonsDisabled: true,
        });

        const res = await fetch('/refresh_ratings', {
            method: 'POST',
            body: JSON.stringify({'do_refresh': true}),
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
        });
        const json = await res.json()
        this.setState({
            forceUpdateButtonText: 'Force update',
            dataButtonsDisabled: false,
        });

        await this.updateData();
    }

    getChartData = () => {
        let {date_labels, average_axis, count_axis} = {...this.state.chartData};

        const limit = 1000;
        let chartData = {
            labels: date_labels.slice(0, limit),
            datasets: [{
                label: 'Averages',
                data: average_axis.slice(0, limit),
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgb(255, 99, 132)',
                fill: false,
                yAxisID: 'y-axis-avg',
            },{
                label: 'Total Ratings',
                data: count_axis.slice(0, limit),
                fill: false,
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgb(54, 162, 235)',
                yAxisID: 'y-axis-count',
            }]
        };

        let chartOptions = {
            responsive: true,
            scales: {
                stacked: false,
                yAxes: [{
                    type: 'linear',
                    position: 'left',
                    display: true,
                    id: 'y-axis-avg',
                }, {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    id: 'y-axis-count',

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            },
        };

        return {chartData, chartOptions};
    }

    render() {
        let {chartData, chartOptions} = {...this.getChartData() };

        return (
            <div>
                <div>
                    <Button color="primary" disabled={this.state.dataButtonsDisabled} onClick={this.updateData}> {this.state.refreshButtonText} </Button>
                    &nbsp;
                    <Button color="secondary" disabled={this.state.dataButtonsDisabled} onClick={this.forceUpdate}> {this.state.forceUpdateButtonText} </Button>
                </div>
                <Line options={chartOptions} data={chartData} />
            </div>
        );
    }
}
