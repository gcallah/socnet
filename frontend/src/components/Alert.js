import React, { Component } from "react";

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
      <div style={{ marginBottom: '15px' }}>
        {eventDetails.map((i) => {
          return <div>{i}</div>
        })}
      </div>
    );
  }
}

export default Alert;