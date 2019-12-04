import React, { Component } from 'react';
import axios from 'axios';
import { Segment, Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';

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
        <Segment>
          <Dimmer active inverted>
            <Loader inverted>Loading</Loader>
          </Dimmer>
        </Segment>
      );
    }

    return (
      <div className="container">
        <Header title="Socnet" />
        {alerts.map((alert) =>{
          return alert
        })}
      </div>
    );
  }
}

export default Home;