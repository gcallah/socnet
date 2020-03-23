import React, { Component } from 'react';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import { Form , Button } from 'react-bootstrap';
import FormInputField from './FormInputField';
import moment from 'moment';
import { Header, Segment } from 'semantic-ui-react';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
      properties: {},
      requiredProperties: [],
      payload: {}
    };

    this.apiServer = 'https://socnet.pythonanywhere.com/';
    
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
    const { history } = this.props;

    Object.keys(payload).map((payloadKey) => {
      if (payloadKey === "event_severity" && payload[payloadKey].value === undefined) {
        payload[payloadKey] = 'Low';
      } else
        payload[payloadKey] = payload[payloadKey].value;
    });

    payload["event_datetime"] = moment().format("YYYY-MM-DD hh:mm:ss");
    console.log("after payload", moment().format("YYYY-MM-DD hh:mm:ss"));
    
    try {
      await axios.post(`${this.apiServer}alerts`, payload);
      history.push('/alerts');
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

  firstLetterUpperCase = (item) => {
    return item[0].toUpperCase() + item.slice(1) + ": "
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
        <Segment basic padded>
          <Header as="h1"> Create Alerts </Header>
          <Header> Please help us stay safe by entering the information about the incident you wish to report.</Header>
        </Segment>
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
                  if (item !== 'event_datetime') {
                    return (
                      <tr> 
                        <td>
                          <label> {this.firstLetterUpperCase(this.formatItem(item))} </label>
                        </td>
                        <td> 
                          <FormInputField
                            label={this.formatItem(item)}
                            type={this.formatType(properties[item].type, properties[item].values)}
                            placeholder={properties[item].example}
                            propChanged={e => this.propChanged(e, item)}
                            values={properties[item].values}
                            key={this.formatItem(item)}
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
      </div>
    );
  }
}

export default Home;
