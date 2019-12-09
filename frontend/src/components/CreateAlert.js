import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';
import { FormControl, Form, Button, InputGroup } from 'react-bootstrap';
import FormInputField from './FormInputField';
import moment from 'react-moment';
class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      properties: {},
      requiredProperties: [],
      payload: {}
    };
    this.apiServer = 'http://socnet.pythonanywhere.com/'

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
      console.log(this.state.form.properties);
    } catch (e) {
      console.log('error')
    }
  }
  propChanged = (e) => {
    const { properties } = this.state;
    const { name, value } = e.target;
    properties[name] = value
    this.setState({
      payload: properties,
    })
  }

  handleSubmit = async(event) => {
    console.log(this.state.payload);
    event.preventDefault();
    const { payload } = this.state;
    const { history } = this.props;
    payload['event_datetime'] = moment(new Date().toLocaleString()).format('YYYY/MM/DD h:mm:ss');
    try {
      const res = await axios.put(`${this.apiServer}alerts`, payload);
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
        <div>
        <Header title="Socnet" />
        </div>
        <form>
          <div className="container">
          <Form className="container-fluid mt-4">
            {Object.keys(properties).map((item) => {
              if (item !== 'event_datetime') {
                return (
                  <InputGroup className="mb-3">
                    <InputGroup.Prepend>
                      <InputGroup.Text id="basic-addon1">
                      {this.formatItem(item)}
                      </InputGroup.Text>
                    </InputGroup.Prepend>
                    <FormControl
                      placeholder={properties[item].example}
                      aria-label="Username"
                      aria-describedby="basic-addon1"
                    />
                  </InputGroup>
                );
              }
            })}
            <Button variant="primary" type="submit">
              Submit Alert
            </Button>
          </Form>
          </div>
        </form>
      </div>
    );
  }
}

export default Home;
