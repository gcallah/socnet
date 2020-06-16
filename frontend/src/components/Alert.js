import React, { Component } from "react";
import { Link } from 'react-router-dom';
import Card from 'react-bootstrap/Card';

class Alert extends Component {
  constructor(props){
    super(props);
    this.state = {
      eventDetails: this.props.data,
    }
    this.background = {
      "Low": "light",
      "Medium": "warning",
      "High": "danger",
    };
    this.bgcolor = {
      "Low": "#FFFFFF",
      "Medium": "#FFCC00",
      "High": "#CC0000",
    }
    this.TITLE = 7
    this.SEVERITY = 8
    this.AUTHOR = 9
  }

  render() {
    const { eventDetails } = this.state;
    const { linkable } = this.props
    return (
      <Card className="m-3">
        <Card.Header style={{background: this.bgcolor[eventDetails[this.SEVERITY]]}}  as="h5">{ eventDetails[6] }</Card.Header>
        <Card.Body>
          <Card.Title>{ eventDetails[this.TITLE] }</Card.Title>
          <Card.Text>
            { `${eventDetails[3]}, ${eventDetails[4]} ${eventDetails[2]}, ${eventDetails[5]} at ${eventDetails[1]}` }
            <br />
            { `Priority: ${eventDetails[this.SEVERITY]}` }
            <br />
            { `Author: ${eventDetails[this.AUTHOR]}` }
          </Card.Text>
          {linkable ? <Link to={`/thread/${this.props.id}`}><button type="button" className="btn btn-dark">View Thread</button></Link> : null}
        </Card.Body>
      </Card>
    );
  }
}

export default Alert;
