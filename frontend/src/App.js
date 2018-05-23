import React, { Component } from 'react';
import { hot } from 'react-hot-loader'

class App extends Component {

    state = {
        hello: ""
    }

    async componentDidMount() {
        const res = await fetch("/hello")
        const json = await res.json()
        this.setState(json)
    }

    render() {
        return (
            <div className="container">
                <h3> Welcome to ZOMBOCOM </h3>
                <p>
                    API Response: {this.state.hello}
                </p>
            </div>
        );
    }
}

export default hot(module)(App)
