import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './styles.css';

class InfoField extends Component {
    async componentDidMount() {
        // here you will use axios.get() for your endpoint
    }


    render() {
        return (
          <>
            Number of alerts: 
          </>
        )
    }
}

export default InfoField;
