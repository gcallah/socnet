import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  render() {
    return (
      <div className="container">
        <Header title="Socnet" />
      </div>
    );
  }
}

export default Home;