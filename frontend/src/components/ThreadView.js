import React, { Component } from 'react';
import axios from 'axios';
import { Icon, Header, Loader, Dimmer, Comment, Form, Button } from 'semantic-ui-react';
import NavBar from './Navbar';
import Alert from './Alert';
import config from '../config';

class ThreadView extends Component {
  constructor(props) {
    super(props)

    this.state = {
      loadingData: false,
      comments: [],
      alert: [],
    }
    // console.log("Constructor: ", this.props.match.params.id )
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      console.log(this.props);

      const res = await axios.get(`${config.API_URL}threads/${this.props.match.params.id}`);
      const alert = await axios.get(`${config.API_URL}alerts/${this.props.match.params.id}`);

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
      console.log(`${config.API_URL}threads/${this.props.match.params.id}`)
      let res = await axios.put(`${config.API_URL}threads/${this.props.match.params.id}`, payload);
      res = await axios.get(`${config.API_URL}threads/${this.props.match.params.id}`);

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
        < NavBar />
        <Alert data={alert} id={alert[0]} />

        <div style={{ textAlign: "left", paddingBlockEnd: 15, paddingBlockStart: 15 }} >
          <Comment.Group>
            <Header as='h3' dividing>
              Comments
            </Header>
            {comments.map((comment, i) => {
              return (
                <Comment>
                  <Comment.Author style={{ fontSize: 15 }}> <Icon name="user" /> Anonymous </Comment.Author>
                  <Comment.Text style={{ fontSize: 15 }}> {comment[Object.keys(comment)[0]]} </Comment.Text>
                </Comment>
              )
            })
            }
            <Form reply>
              <Form.Input placeholder="Type your comment here." onChange={this.propChanged} />
              <Button content='Add Comment' labelPosition='left' icon='edit' primary onClick={e => this.handleSubmit(e)} />
            </Form>
          </Comment.Group>
        </div>

        {/* <ListGroup>
          {comments.map((comment, i) => {
            return (
              <ListGroup.Item key={i}>{comment[Object.keys(comment)[0]]}</ListGroup.Item>
            )
          })}
        </ListGroup>
        
        <InputGroup>
          <InputGroup.Prepend>
            <InputGroup.Text>Add a comment</InputGroup.Text>
          </InputGroup.Prepend>
          <FormControl onChange={this.propChanged} as="textarea" aria-label="Add a comment" />
          <Button variant="dark" type="submit" onClick={e => this.handleSubmit(e)}>Submit Comment</Button>
        </InputGroup>
        <br/> 
        <br /> */}
        
        {/*  Dennis' Code: */}
        {/* <div class="col-auto">
        <div class="form-check form-check-inline">
        <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1"></input>
        <label class="form-check-label" for="inlineRadio1">1</label>
        </div> 
        </div> */}

      </div>
    );
  }
}

export default ThreadView;
