import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import config from '../config';
import './styles.css';


class InfoField extends Component {
    render() {
        const payload = axios.get(`${config.API_URL}number_of_alerts`);
        // const numAlerts = payload.data.number_of_alerts
        return (
          <>
            Number of alerts:
          </>
        )
    }
}

export default InfoField;
