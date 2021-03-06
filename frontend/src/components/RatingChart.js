import React from 'react';
import toastr from 'toastr';
import './toastr.min.css';
// import PropTypes from 'prop-types';

import { Button, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';
import { Line } from 'react-chartjs-2';

const JSON_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};

toastr.options = {
    "positionClass": "toast-bottom-full-width",
};

class RatingDateFilterDropdown extends React.Component {
    titleCaseDateFilter() {
        let dateFilter = this.props.currentDateFilter;
        return dateFilter[0].toUpperCase() + dateFilter.substring(1)
    }

    render() {
        return (
            <UncontrolledDropdown>
                <DropdownToggle caret>
                    <small>Range:</small> { this.titleCaseDateFilter() }
                </DropdownToggle>
                <DropdownMenu>
                    <DropdownItem onClick={() => { this.props.setDateRange('all'); } }>All Time</DropdownItem>
                    <DropdownItem onClick={() => { this.props.setDateRange('year'); } }>Last Year</DropdownItem>
                    <DropdownItem onClick={() => { this.props.setDateRange('month'); } }>Last Month</DropdownItem>
                    <DropdownItem onClick={() => { this.props.setDateRange('week'); } }>Last Week</DropdownItem>
                    <DropdownItem onClick={() => { this.props.setDateRange('day'); } }>Last Day</DropdownItem>
                </DropdownMenu>
            </UncontrolledDropdown>
        );
    };
};

export default class RatingChart extends React.Component {
    state = {
        chartData: {
            date_labels: [],
            average_axis: [],
            count_axis: [],
        },
        currentAverage: "N/A",
        refreshButtonText: 'Refresh',
        forceUpdateButtonText: 'Force Update',

        dateFilter: 'all',

    }

    updateData = async () => {
        let firstLoad = this.state.chartData.date_labels.length === 0; //hack to not show the toast the first time
        this.setState({
            refreshButtonText: 'Refreshing...',
            dataButtonsDisabled: true,
        });

        let dateFilter = new URLSearchParams({'date_filter': this.state.dateFilter});
        const res = await fetch(`/fetch_ratings?${dateFilter.toString()}`);
        const json = await res.json();

        if (!firstLoad) {
            toastr.success("Refreshed chart!");
        };

        this.setState({
            chartData: json.chart_data,
            refreshButtonText: 'Refresh',
            dataButtonsDisabled: false,
            currentAverage: json.current_average,
        })
    }

    setIntervalUpdate = () => {
        this.forceUpdateInterval = setInterval(() => {
            this.forceUpdate();
        }, 1000*60*60);
    }

    componentDidMount = async () => {
        this.setIntervalUpdate()

        this.updateData();
    }

    componentWillUnmount = () => {
        clearInterval(this.forceUpdateInterval);
    }

    forceUpdate = async () => {
        clearInterval(this.forceUpdateInterval);
        this.setIntervalUpdate();

        this.setState({
            forceUpdateButtonText: 'Forcing update...',
            dataButtonsDisabled: true,
        });

        const res = await fetch('/refresh_ratings', {
            method: 'POST',
            body: JSON.stringify({'do_refresh': true}),
            headers: JSON_HEADERS,
        });
        const json = await res.json()

        if (json.success) {
            toastr.success(json.message);
        } else {
            toastr.warning(json.message);
        };

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
                label: "New Ratings",
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

    setDateRange = (dateFilter) => {
        console.log("setting datefilter");
        this.setState({
            dateFilter: dateFilter,
        }, this.updateData);
    };

    render() {
        let {chartData, chartOptions} = {...this.getChartData() };

        return (
            <div>
                <div className="row">
                    <div className="col h5 justify-content-start" > Current Average: {this.state.currentAverage} </div>
                    <div className="col a justify-content-end">
                        <Button className="float-right" color="primary" disabled={this.state.dataButtonsDisabled} onClick={this.updateData}> {this.state.refreshButtonText} </Button>
                        <Button className="float-right" color="secondary" disabled={this.state.dataButtonsDisabled} onClick={this.forceUpdate}> {this.state.forceUpdateButtonText} </Button>
                        <span className="float-right">
                            <RatingDateFilterDropdown currentDateFilter={this.state.dateFilter} setDateRange={this.setDateRange}className="" />
                        </span>
                    </div>
                </div>
                <Line options={chartOptions} data={chartData} />
            </div>
        );
    }
}
