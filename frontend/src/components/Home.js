import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import ThreadAlerts from './ThreadAlerts';
import './styles.css';
import NavBar from './Navbar';
import InfoField from './InfoField';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
    };
  }


  render() {
    const loadingData  = this.state.loadingData;

    // while fetching data from the API
    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading</Loader>
        </Dimmer>
      );
    }


    return (

      <div className="container">
          {}
        <NavBar />
        <InfoField />
        <ThreadAlerts />
      </div>
    );
  }
}

export default Home;
