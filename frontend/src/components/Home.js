import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import ThreadAlerts from './ThreadAlerts';
import './styles.css';
import NavBar from './Navbar';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
    };
    this.apiServer = 'https://socnet.pythonanywhere.com/'
  }

  //  Fetching alerts is now handled in the new component "ThreadAlerts" or "FilterForm"
  // async componentDidMount() {
  //   try {
  //     this.setState({ loadingData: true });
  //     // get the alerts from the server
  //     const res = await axios.get(`${this.apiServer}alerts`);
  //     // add them to the state
  //     this.setState({
  //       alerts: res.data,
  //       loadingData: false,
  //     })
  //     console.log(this.state);
  //   } catch (e) {
  //     console.log('error')
  //   }
  // }

  render() {
    const loadingData  = this.state.loadingData;

    // while fetching data from the API
    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading</Loader>
        </Dimmer>
      );
    }


    return (

      <div className="container">
          {/* <Header title="Socnet" className="main-title"/>
            <Link to='/createAlert'><button type="button" className="btn btn-primary">Create Alert</button></Link>
            <Link to='/'><button type="button" className="btn btn-primary">Filter Results</button></Link> */}
        < NavBar />
        <ThreadAlerts />
      </div>
    );
  }
}

export default Home;