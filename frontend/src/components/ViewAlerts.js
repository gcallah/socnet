import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import AlertsTable from './AlertsTable';
import './styles.css';
import NavBar from './Navbar';
import axios from 'axios';
import config from '../config';
import InfoField from './InfoField';

class ViewAlerts extends Component {
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
      let alertsReq = axios.get(`${config.API_URL}number_of_alerts`);
      let earliestReq = axios.get(`${config.API_URL}oldest_alert`);
      let latestReq = axios.get(`${config.API_URL}newest_alert`);
      axios.all([alertsReq, earliestReq, latestReq]).then(axios.spread((...responses) => {
        const numAlerts = responses[0]
        const earliest = responses[1]
        const latest = responses[2]

        this.setState({
          numAlerts: numAlerts.data,
          earliest : earliest.data,
          latest :  latest.data,
          loadingData: false,
        })
      }));

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
        {/* <InfoField label={"Earliest alert posted"} data={this.state.earliest.oldest_alert}/> */}
        </div>
        <InfoField label={"Number of alerts"} data={this.state.numAlerts.number_of_alerts}/>
        <div id='right'>
        {/* <InfoField label={"Lastest alert posted"} data={this.state.latest.newest_alert}/> */}
        </div>
        <AlertsTable />
      </div>
    );
  }
}

export default ViewAlerts;
