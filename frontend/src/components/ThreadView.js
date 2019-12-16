import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import { useParams } from 'react-router-dom';
import Header from './Header';

class ThreadView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      comments: [],
    }
    this.apiServer = 'http://socnet.pythonanywhere.com/'
  };

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      console.log(this.props);
      console.log(`${this.apiServer}threads/${this.state.id}`);
      const res = await axios.get(`${this.apiServer}threads/${this.props.match.params.id}`);
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

export default ThreadView;