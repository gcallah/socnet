import React, { Component } from "react";
import Card from 'react-bootstrap/Card';

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
        <div style={{ marginBottom: '15px' }}>
          {eventDetails.map((i) => {
            return <div>{i}</div>
          })}
        </div>
      </Card>
    );
  }
}

export default Alert;