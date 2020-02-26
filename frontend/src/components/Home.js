import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';
import Alert from './Alert';
import ThreadAlerts from './ThreadAlerts';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      alerts: [],
    };
    this.apiServer = 'https://socnet.pythonanywhere.com/'
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      // get the alerts from the server
      const res = await axios.get(`${this.apiServer}alerts`);
      // add them to the state
      this.setState({
        alerts: res.data,
        loadingData: false,
      })
      console.log(this.state);
    } catch (e) {
      console.log('error')
    }
  }

  render() {
    const { loadingData, alerts } = this.state

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
        <Header title="Socnet" />
        <Link to='/createAlert'><button type="button" className="btn btn-primary">Create Alert</button></Link> <br /> <br />
        <Link to='/filterAlert'><button type="button" className="btn btn-primary">Filter Results</button></Link>
        {/* {alerts.map((alert) =>{
          return (

            /// TO-DO: Change this to be just the alert title as a button in the component
            <Alert
              data={alert}
              key={alert[0]}
              id={alert[0]}
              linkable
            />
          )
        })} */}
        <ThreadAlerts />
      </div>
    );
  }
}

export default Home;