import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';

class ThreadView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      comments: [],
    }
    this.apiServer = 'https://socnet.pythonanywhere.com/'
  };

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      console.log(this.props);
      const res = await axios.get(`${this.apiServer}threads/${this.props.match.params.id}`);
      this.setState({
        comments: res.data,
        loadingData: false,
      })
      console.log(this.state.comments);
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
        {comments.map((comment, i) => {
          return(
            <div key={i}>{comment[Object.keys(comment)[0]]}</div>
          )
        })}
      </div>
    );
  }
}

export default ThreadView;