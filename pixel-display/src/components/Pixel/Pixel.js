import React, { Component } from 'react';
import './Pixel.css';

class Pixel extends Component {

	getHex(value) {
		// value = (255 - value); // If you want to invert the colours.
		var hexValue = value.toString(16);
		if (hexValue.length === 1) {
			hexValue = `0${hexValue}`;
		}
		return hexValue;
	}

	getHexColour() {
		const value = this.props.value;

		const red = value & 0xFF;
		const green = (value >> 8) & 0xFF;
		const blue = (value >> 16) & 0xFF;

		return '#' + this.getHex(red) + this.getHex(green) + this.getHex(blue);
	}

	render() {
		return (
			<div className="Pixel" style={{backgroundColor: this.getHexColour() }}/>
		);
	}
}

export default Pixel;
