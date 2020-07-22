import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';
import { Loader, Dimmer, Header, Segment } from 'semantic-ui-react';
import { Form , Button } from 'react-bootstrap';
import CustomSnackbar from './Snackbar';
import config from '../config';

import NavBar from './Navbar';
import FormInputField from './FormInputField';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      properties: {},
      requiredProperties: [],
      payload: {},
      open: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      const res = await axios.get(`${config.API_URL}form`);
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
    const { value } = e.target;
    console.log("props changed properties ", properties);
    properties[item].value = value;
    this.setState({
      payload: properties,
    })
  }

  handleSubmit = async(event) => {
    console.log("event is ", this.inputNode);
    console.log("before payload", this.state.payload);
    event.preventDefault();

    const { payload } = this.state;
    //const { history } = this.props;

    Object.keys(payload).map((payloadKey) => {
      if (payloadKey === "severity" && payload[payloadKey].value === undefined) {
        return payload[payloadKey] = 'Low';
      } else
        return payload[payloadKey] = payload[payloadKey].value;
    });

    payload["datetime"] = moment().format("YYYY-MM-DD hh:mm:ss");
    console.log("after payload", moment().format("YYYY-MM-DD hh:mm:ss"));

    try {
      await axios.post(`${config.API_URL}alerts`, payload);
      this.setState({open: true})
      // Commented by Harman Chawla.
      // Uncomment this (and line 57) if you want to redirect the user to alerts table
      // when an alert is created.
      //history.push('/alerts');
    } catch (e) {
      console.log(e)
    }
  }

  formatType = (type, values) => {
    if (typeof values === "undefined") {
      if (type === "datetime") {
        return "datetime-local";
      } else {
        return "text";
      }
    } else {
      return "select";
    }
  };

  firstLetterUpperCase = (elem) => {
    return elem[0].toUpperCase() + elem.slice(1) + ": "
  }

  render() {
    const { loadingData, properties, errorMessage } = this.state

    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading</Loader>
        </Dimmer>
      );
    }

    return (

      <div className="container">
        < NavBar />
        <Segment basic padded>
          <Header as="h1"> Create Alerts </Header>
          <Header> Please help us stay safe by entering the information about the incident you wish to report.</Header>
        </Segment>
      {/* Commenting the code below. Deprecated in favor of the new UI. */}
      {/* <div className="container mt-5">
      <Segment placeholder>
        <Header icon>
          <Icon name='shield alternate' circular/>
          Please help us stay safe by entering the information about the incident you wish to report.
        </Header>
        </Segment>
      </div> */}
        <Segment padded='very' raised color='teal'>
          <Form className="container-fluid mt-4" onSubmit={e => this.handleSubmit(e)}>
            <table align="center" cellPadding="5px">
              <tbody>
                {Object.keys(properties).map((item) => {
                  //console.log(item);
                  if (item !== 'datetime') {
                    return (
                      <tr>
                        <td style={{textAlign: "left"}}>
                          <label> { this.firstLetterUpperCase(item) } </label>
                        </td>
                        <td>
                          <FormInputField
                            // label={this.formatItem(item)}
                            type={this.formatType(properties[item].type, properties[item].values)}
                            placeholder={properties[item].example}
                            propChanged={e => this.propChanged(e, item)}
                            values={properties[item].values}
                            // key={this.formatItem(item)}
                            errorMessage={errorMessage}
                          ></FormInputField>
                        </td>
                      </tr>
                    );
                  }
                })}
              </tbody>
            </table>
            <Button type="submit"> Submit Alert  </Button>
          </Form>
        </Segment>
        <CustomSnackbar open={this.state.open} message="Successfully created!"/>
      </div>
    );
  }
}

export default Home;
