import React, { Component } from 'react';

import Line from '../Line/Line'

import './App.css';

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}


function generateLine() {
	var data = [];
	for (var i = 0; i < 64; i++) 
		data.push(getRandomInt(16777215));

	return data;
}

function testData() {
	var data = [];

	for (var i = 0; i < 64; i++)
		data.push(generateLine());

	return data;
}


class App extends Component {

	getData() {
		fetch('http://127.0.0.1:8080/albumart')
      		.then(response => response.json())
      		.then(data => this.setState({ data }));
	}

	constructor(props) {
		super(props);
		this.state = { data: testData() };
		this.getData()
	}

	componentDidMount() {
		this.interval = setInterval(() => this.getData(), 3000);
	}

	componentWillUnmount() {
		clearInterval(this.interval);
	}

	renderLines() {
		return this.state.data.map(this.renderLine);
	}

	renderLine(lineData) {
		return <Line data={lineData}/>;
	}

	render() {
		return (
			<div className="App">
				<div className="Content">
					{this.renderLines()}
				</div>
			</div>
		);
	}
}

export default App;
