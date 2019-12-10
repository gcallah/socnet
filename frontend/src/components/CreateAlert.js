import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import { FormControl, Form, Button, InputGroup, Card } from 'react-bootstrap';
import FormInputField from './FormInputField';
import moment from 'moment';
import { Header, Icon, Image, Segment } from 'semantic-ui-react';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      properties: {},
      requiredProperties: [],
      payload: {}
    };

    this.apiServer = 'http://socnet.pythonanywhere.com/';
    this.handleSubmit = this.handleSubmit.bind(this);

  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      const res = await axios.get(`${this.apiServer}form`);
      this.setState({
        properties: res.data.properties,
        requiredProperties: res.data.required,
        loadingData: false,
      })
    } catch (e) {
      console.log('error')
    }
  }
  propChanged = (e, item) => {

    const { properties } = this.state;
    const { name, value } = e.target;
    console.log("props changed properties ", properties);
    properties[item] = value;
    this.setState({
      payload: properties,
    })
  }

  handleSubmit = async(event) => {
    console.log("event is ", this.inputNode);
    console.log("before payload", this.state.payload);
    event.preventDefault();
    const { payload } = this.state;
    const { history } = this.props;

    payload["event_datetime"] = moment(new Date().toLocaleString()).format('YYYY/MM/DD h:mm:ss');
    console.log("after payload", payload);
    try {

      const res = await axios.post(`${this.apiServer}alerts`, payload);
      history.push('/');

    } catch (e) {
      console.log(e)
    }

  }
  formatItem = (item) => {
    if (item.includes("event")){
      item=item.substring(6,item.length);
    }
    else {
      item="sender's name";
    }
    return item;
  }
  render() {
    const { loadingData, properties, requiredProperties } = this.state

    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading</Loader>
        </Dimmer>
      );
    }

    return (

      <div className="container">
      <div className="container mt-5">
      <Segment placeholde >
        <Header icon>
          <Icon name='shield alternate' circular/>
          Please help us stay safe by entering the information about the incident you wish to report.
        </Header>
        </Segment>
      </div>
        <form>
          <div className="container" style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '60vh'}} >
          <Form className="container-fluid mt-4">
            {Object.keys(properties).map((item) => {
              if (item !== 'event_datetime') {
                return (
                  <InputGroup className="mb-3">
                    <InputGroup.Prepend>
                      <InputGroup.Text id="basic-addon1">{this.formatItem(item)}</InputGroup.Text>
                    </InputGroup.Prepend>
                    <FormControl
                      placeholder={properties[item].example}
                      aria-label="Username"
                      aria-describedby="basic-addon1"
                      onChange={e => this.propChanged(e, item)}
                    />
                  </InputGroup>
                );
              }
            })}
            <Button variant="outline-secondary" type="submit" onClick= {e => this.handleSubmit(e)}>Submit Alert</Button>
          </Form>
          </div>
        </form>
      </div>
    );
  }
}

export default Home;
