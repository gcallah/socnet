import React, { Component } from "react";
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

class Alert extends Component {
  constructor(props){
    super(props);
    this.state = {
      eventDetails: this.props.data,
    }
  }

  render() {
    const { eventDetails } = this.state;
    return (
      <Card>
        <Card.Header as="h5">{ eventDetails[0] }</Card.Header>
        <Card.Body>
          <Card.Title>{ eventDetails[6] }</Card.Title>
          <Card.Text>
            { eventDetails[7] }
          </Card.Text>
          <Button variant="dark">View Thread</Button>
        </Card.Body>
      </Card>
    );
  }
}

export default Alert;