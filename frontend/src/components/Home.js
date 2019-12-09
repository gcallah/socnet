import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';
import Alert from './Alert';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      alerts: [],
    };
    this.apiServer = 'http://socnet.pythonanywhere.com/'
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      const res = await axios.get(`${this.apiServer}alerts`);
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
        {alerts.map((alert) =>{
          return (
            <Alert
              data={alert}
              key={alert[0]}
            />
          )
        })}
      </div>
    );
  }
}

export default Home;