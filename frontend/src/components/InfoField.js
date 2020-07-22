import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './styles.css';


class InfoField extends Component {
/*
 * We need a constructor that gets passed:
 *   * label
 *   * data
 *   For ex., see Alert.js
 *   Line 83 in ThreadView.js shows the use of the constructor.
 */
  constructor(props){
    super(props);
    this.state = {
      eventDetails: this.props.data,
    }
  }


  state = {
    numAlerts: ""
  };

    render() {
        return (
          <>
            {`${this.props.label}`}: {this.props.data}
          </>
        )
    }
}

export default InfoField;
