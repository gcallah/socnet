import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';

class ThreadView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      threadId: this.props.id,
      comments: [],
    }
    this.apiServer = 'http://socnet.pythonanywhere.com/'
  };

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      const res = await axios.get(`${this.apiServer}threads/${this.threadId}`);
      this.setState({
        comments: res,
        loadingData: false,
      })
      console.log(this.state);
    } catch (e) {
      console.log('error')
    }
  }

  render() {
    const { loadingData, comments } = this.state;

    if (loadingData) {
      return(
        <Dimmer active inverted>
          <Loader size="massive">Loading</Loader>
        </Dimmer>
      );
    }

    return (
      <div className="container">
        <Header title="Socnet" />
        
      </div>
    );
  }
}