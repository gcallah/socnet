import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import config from '../config';
import './styles.css';


class InfoField extends Component {
  
  state = {
    numAlerts: ""
  };
  
 async componentDidMount() {
  try {
      axios.get(`${config.API_URL}number_of_alerts`)
      .then( payload => {
          this.setState({numAlerts: payload.data})
      // .catch: (perhaps?) to handle 404 etc.
      });
  } catch (e) {
      console.log("Unable to fetch number of alerts.")
  }
}

    render() {
        return (
          <>
            Number of alerts: {this.state.numAlerts.number_of_alerts}
          </>
        )
    }
}

export default InfoField;
