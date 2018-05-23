import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { hot } from 'react-hot-loader'

class ReviewData extends Component {
    static propTypes = {
        ratings: PropTypes.number.isRequired,
    }

    render() {
        return (
            <div>
                <span> Rating {this.props.ratings} </span>
            </div>
        );
    }
};

class App extends Component {

    state = {
        currentData: {
            results: [],
            timestamp: '',
        }
    }

    async componentDidMount() {
        const res = await fetch("/hello")
        const json = await res.json()
        this.setState({
            currentData: json.current_data
        })
    }

    render() {
        return (
            <div className="container">
                <h3> Welcome to ZOMBOCOM </h3>
                <div>
                    { this.state.currentData.results.map((ratings, i) => {
                        return ( <ReviewData key={i} ratings={ratings.rating} /> );
                    }) }
                </div>
            </div>
        );
    }
}

export default hot(module)(App)
