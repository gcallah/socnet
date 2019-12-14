import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import { Form, Button } from 'react-bootstrap';
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
      <style>{'body { background-color: grey; }'}</style>
      <Segment placeholde >
        <Header icon>
          <Icon name='shield alternate' circular/>
          Please help us stay safe by entering the information about the incident you wish to report.
        </Header>
        </Segment>
      </div>
          <Form className="container-fluid mt-4">
            {Object.keys(properties).map((item) => {
              return (
                <FormInputField
                  label={this.formatItem(item)}
                  type={properties[item].type}
                  placeholder={properties[item].example}
                  propChanged={e => this.propChanged(e, item)}
                ></FormInputField>
              );
            })}
            <Button variant="dark" type="submit" onClick= {e => this.handleSubmit(e)}>Submit Alert</Button>
          </Form>
      </div>
    );
  }
}

export default Home;
