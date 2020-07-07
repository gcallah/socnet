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
      earliestAlert: '',
      latestAlert: '',
      loadingData: false,
    };
  }
 
 async componentDidMount() {
   try {
      this.setState({ loadingData: true });
      let payload = await axios.get(`${config.API_URL}number_of_alerts`);
      let earliest = await axios.get(`${config.API_URL}oldest_alert`);
      let latest = await axios.get(`${config.API_URL}newest_alert`);
      axios.all([payload, earliest, latest]).then(axios.spread((responses) => {
        let payload = responses[0]
        let earliest = responses[1]
        let latest = responses[2]
      }));

      this.setState({
        numAlerts: payload.data,
        earliestAlert : earliest.data,
        latestAlert :  latest.data,
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
    return (
      <div className="container">
          {}
        <NavBar />
        <div id='left'>
        <InfoField label={"Earliest alert posted"} data={this.state.earliestAlert.oldest_alert}/>
        </div>
        <InfoField label={"Number of alerts"} data={this.state.numAlerts.number_of_alerts}/>
        <div id='right'>
        <InfoField label={"Lastest alert posted"} data={this.state.latestAlert.newest_alert}/>
        </div>
        <ThreadAlerts />
      </div>
    );
  }
}

export default Home;
