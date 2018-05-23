import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'

class ReviewData extends Component {
    static propTypes = {
        rating: PropTypes.number.isRequired,
    }

    render() {
        return (
            <div>
                <span> Rating {this.props.rating} </span>
            </div>
        );
    }
};

class App extends Component {
    state = {
        ratings: [],
        timestamp: '',
    }

    async componentDidMount() {
        const res = await fetch("/ratings")
        const json = await res.json()
        this.setState({
            ratings: json.ratings
        })
    }

    render() {
        return (
            <div className="container">
                <h3> Welcome to ZOMBOCOM </h3>
                <div>
                    { this.state.ratings.slice(0, 10).map((data, i) => {
                        return ( <ReviewData key={i} raw_data={data} rating={data.rating_score} /> );
                    }) }
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
