import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import ThreadAlerts from './ThreadAlerts';
import './styles.css';
import NavBar from './Navbar';
import axios from 'axios';
import config from '../config';
import InfoField from './InfoField';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      numAlerts: 0,
      loadingData: false,
    };
  }

  
 async componentDidMount() {
   try {
      this.setState({ loadingData: true });
      let payload = await axios.get(`${config.API_URL}number_of_alerts`)
      this.setState({
        numAlerts: payload.data,
        loadingData: false,
      })
   } catch (e) {
       console.log("Unable to fetch number of alerts.")
       this.setState({ loadingData: false });
   }
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


    // another field: <InfoField label={"Earliest alert"}/>
    return (

      <div className="container">
          {}
        <NavBar />
        <InfoField label={"Number of alerts"} data={this.state.numAlerts.number_of_alerts}/>
        <ThreadAlerts />
      </div>
    );
  }
}

export default Home;
