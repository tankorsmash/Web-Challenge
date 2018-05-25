import React from 'react';
import PropTypes from 'prop-types';
import { Line } from 'react-chartjs-2';

export default class RatingChart extends React.Component {
    static propTypes = {
        dateLabels: PropTypes.array.isRequired,
        averageAxis: PropTypes.array.isRequired,
        countAxis: PropTypes.array.isRequired,
    }

    render() {
        let {dateLabels, averageAxis, countAxis} = {...this.props};

        const limit = 1000;
        let chartData = {
            labels: dateLabels.slice(0, limit),
            datasets: [{
                label: "Averages",
                data: averageAxis.slice(0, limit),
                borderColor: "rgb(255, 99, 132)",
                backgroundColor: "rgb(255, 99, 132)",
                fill: false,
                yAxisID: "y-axis-avg",
            },{
                label: "Total Ratings",
                data: countAxis.slice(0, limit),
                fill: false,
                borderColor: "rgb(54, 162, 235)",
                backgroundColor: "rgb(54, 162, 235)",
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
            <div>
                <Line  options={chartOptions} data={chartData} />
            </div>
        );
    }
}
