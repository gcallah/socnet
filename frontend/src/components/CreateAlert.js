import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Loader, Dimmer } from 'semantic-ui-react';
import Header from './Header';
import FormInputField from './FormInputField';

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

  handleSubmit = () => {
    console.log(this.state.payload);
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
        <Header title="Socnet" />
        <form>
          <div className="container">
            {Object.keys(properties).map((item) => {
              if (item !== 'event_datetime') {
                return (
                  <FormInputField
                    label={item}
                    type={properties[item].type}
                    placeholder={properties[item].example}
                    name={item}
                    key={item}
                    propChanged={this.propChanged}
                  />
                );
              }
            })}
          </div>
          <Link to="/"><button onClick={this.handleSubmit} type="button" className="btn btn-primary">Create</button></Link>
        </form>
      </div>
    );
  }
}

export default Home;