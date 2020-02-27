import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';
import Alert from './Alert';
import { ListGroup, InputGroup, FormControl, Button } from 'react-bootstrap';

class ThreadView extends Component {
  constructor(props) {
    super(props)

    this.state = {
      loadingData: false,
      comments: [],
      alert: [],
    }
    // console.log("Constructor: ", this.props.match.params.id )
    this.apiServer = 'https://socnet.pythonanywhere.com/'
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      console.log(this.props);

      const res = await axios.get(`${this.apiServer}threads/${this.props.match.params.id}`);
      const alert = await axios.get(`${this.apiServer}alerts/${this.props.match.params.id}`);

      this.setState({
        comments: res.data,
        loadingData: false,
        alert: alert.data[0],
      })

      console.log(this.state.comments);
    } catch (e) {
      console.log('error')
    }
  }

  propChanged = (e) => {
    const { value } = e.target;
    console.log(value)
    const payload = { "text": value }
    this.setState({
      payload: payload,
    })
  }

  handleSubmit = async(event) => {
    event.preventDefault();
    const { payload } = this.state;

    try {
      this.setState({ loadingData: true });
      console.log(`${this.apiServer}threads/${this.props.match.params.id}`)
      let res = await axios.put(`${this.apiServer}threads/${this.props.match.params.id}`, payload);
      res = await axios.get(`${this.apiServer}threads/${this.props.match.params.id}`);

      this.setState({
        comments: res.data,
        loadingData: false,
      })
    } catch (e) {
      console.log(e)
    }
  }

  render() {
    const { loadingData, comments, alert } = this.state;

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
        
        <Alert data={alert} id={alert[0]} />

        <ListGroup>
          {comments.map((comment, i) => {
            return(
              <ListGroup.Item key={i}>{comment[Object.keys(comment)[0]]}</ListGroup.Item>
            )
          })}
        </ListGroup>
        <InputGroup>
          <InputGroup.Prepend>
            <InputGroup.Text>Add a comment</InputGroup.Text>
          </InputGroup.Prepend>
          <FormControl onChange={this.propChanged} as="textarea" aria-label="Add a comment" />
          <Button variant="dark" type="submit" onClick= {e => this.handleSubmit(e)}>Submit Comment</Button>
        </InputGroup>
      </div>
    );
  }
}

export default ThreadView;
