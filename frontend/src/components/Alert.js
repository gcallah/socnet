import React, { Component } from "react";
import { Link } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import flds, { colors } from '../fields';

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
      "Low": colors.WHITE,
      "Medium": colors.YELLOW,
      "High": colors.RED,
    }
  }
  render() {
    const { eventDetails } = this.state;
    const { linkable } = this.props
    return (
      <Card className="m-3">
        <Card.Header style={{background: this.bgcolor[eventDetails[flds.SEVERITY]]}}  as="h5"> {eventDetails[flds.TYPE]} </Card.Header>
        <Card.Body>
          <Card.Title>{ eventDetails[flds.DESC] }</Card.Title>
          <Card.Text>
            { `${eventDetails[flds.CITY]}, ${eventDetails[flds.STATE]}
            ${eventDetails[flds.ZIP]}, ${eventDetails[flds.COUNTRY]}
            at ${eventDetails[flds.DATE]}` }
            <br />
            { `Priority: ${eventDetails[flds.SEVERITY]}` }
            <br />
            { `Author: ${eventDetails[flds.AUTHOR]}` }
          </Card.Text>
          {linkable ? <Link to={`/thread/${this.props.id}`}><button type="button" className="btn btn-dark">View Thread</button></Link> : null}
        </Card.Body>
      </Card>
    );
  }
}

export default Alert;
