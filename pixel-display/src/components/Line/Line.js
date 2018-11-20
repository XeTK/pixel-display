import React, { Component } from 'react';

import Pixel from '../Pixel/Pixel'

import './Line.css';

class Line extends Component {

	renderPixels() {
		var data = this.props.data;
		return data.map(this.renderPixel);
	}

	renderPixel(value) {
		return <Pixel value={value}/>;
	}

	render() {
		return (
			<div className="Line">
			{this.renderPixels()}
			</div>
		);
	}
}

export default Line;
