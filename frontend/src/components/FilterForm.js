import React, { Component } from 'react';
import { Dimmer, Loader, Grid, Button, Form, Header, Icon, Segment } from 'semantic-ui-react';
import { withRouter } from 'react-router-dom';

import "./Filters.css"

import axios from 'axios';
import DropdownList from "./DropdownList";
import NavBar from './Navbar';
import createHistory from "history/createBrowserHistory";


const history = createHistory();

class FilterForm extends Component {
    state = {
        loading: false,
        date: "", 
        severity: [], 
        type: [],
        region: [], 
        filters: ""
    };
    
    apiServer = 'https://socnet.pythonanywhere.com/';
    // devApiServer = "http://127.0.0.1:8000/";

    async componentDidMount() {
        try {
            axios.get(`${this.apiServer}filters`)
            .then( payload => {
                this.setState({filters: payload.data})
                //this.transformFilterData();
            });
        } catch (e) {
            console.log("Unable to fetch values for the filter form.")
        }

    }


    // Sample Input: Development time only
    severityList = {
        name: "severity",
        type: "dropdown",
        optionList: [{key: "H", text: "High", value: "High"}, 
                    {key: "L", text: "Low", value: "Low"}, 
                    {key: "M", text: "Medium", value: "Medium"}]
    };

    regionList = {
        name: "region", 
        type: "dropdown", 
        optionList: [{key: "NY", text: "NY - New York", value: "New York"}, 
                    { key: "NJ", text: "NJ - New Jersey", value: "New Jersey" },
                    { key: "CT", text: "CT - Conneticut", value: "Conneticut" }]
    };

    typeList = {
        name: "type",
        type: "dropdown",
        optionList: [{ key: "Fire", text: "Fire", value: "Fire" },
        { key: "Earthquake", text: "Earthquake", value: "Earthquake" },
        { key: "Ransomware", text: "Ransomware", value: "Ransomware" },
        { key: "Malware", text: "Malware", value: "Malware"}]
    }

    handleDropdown = (name, value) => {
        this.setState({[name]: value}, () => {
            console.log(name, value);
            console.log("Data changed by dropdown")
            console.log(this.state.severity)
        });
    };
    
    // Excecuted when the back button is clicked
    handleBack = () => {
        // Soon to be depreciated
        this.props.history.push('/alerts')
    }

    handleChange = (e, {name, value}) => { 
        this.setState({[name]:value})
    }

    handleValidation = () => {
        let fields = {
            date: this.state.date,
            severity: this.state.severity,
            type: this.state.type,
            region: this.state.region
        };

        if (fields["date"] || fields["severity"].length > 0 || fields["type"].length > 0 || fields["region"].length > 0) {
            console.log("User chose a filter!")
            return true
        } else {
            return false
        }
    }

    generateQueryString = () => {
        const { loading, date, severity, type, region } = this.state;
        var queryString = [];
        
        if (region.length > 0) {
            queryString.push("region="+region.toString());
        }
        
        if (type.length > 0) {
            queryString.push("type="+type.toString());
        }

        if (severity.length > 0) {
            queryString.push("severity=" + severity.toString());
        }

        if (date.length > 0) {
            queryString.push("date="+date)
        }

        queryString = queryString.join("&");
        return queryString
    }

    handleSubmit = async e => {
        e.preventDefault()
        if (this.handleValidation()) {
            try {
                const queryParams = this.generateQueryString()
                console.log("Query Parameters: ", queryParams)

                await axios.get(`${this.apiServer}alerts?${queryParams}`)
                    .then(payload => {
                        this.setState({ loading: false });
                        this.props.history.push('/alerts', { alerts: payload.data });
                    });
            } catch (e) {
                console.log("ERROR: UNABLE TO FETCH FILTERED RESULTS")
            }
        } else {
            // The user has not added any valid entries to the form
            console.log("The form had no entries. Attempting to load all alerts.")
            try {
                // this.setState({ loading: true });
                await axios.get(`${this.apiServer}alerts`)
                .then (
                    payload => { this.setState({ loading: false, });
                    console.log("Alerts loaded. Payload looks like: ", payload.data)
                    this.props.history.push('/alerts', {alerts: payload.data})
                })
                
            } catch (e) {
                console.log('ERROR: UNABLE TO GET ALL RESULTS.')
            }
        }
    }

    render() {

        const loading = this.state.loading;

        if (loading) {
            return (
                <Dimmer active inverted>
                    <Loader size="massive"> Loading: fetching alerts..</Loader>
                </Dimmer>
            )
        }

        return (
            <div class="container">
                < NavBar />
                <Segment basic padded>
                    <Header as="h1"> Filter Alerts </Header>
                    <Header> Leave all fields blank to see all results.</Header>
                </Segment>
                <Segment padded='very' raised color='teal'>
                    <Grid centered>
                        <Form loading={loading} onSubmit={this.handleSubmit.bind(this)} size="large" style={{ width: "60%" }} autoComplete="on">
                            <table align="center" className="filters" cellPadding="5px">
                                <tbody>
                                    {/* Date */}
                                    <tr>
                                        <td> <label> Since (Date): </label>  </td>
                                        <td>
                                            {/* TO-DO: Input type date doesn't work with Safari and IE. */}
                                            {/* Work around: Text input is formated into a datetime at the backend */}
                                            <input type="date" placeholder="mm/dd/yyyy"
                                                onChange={(event) => this.setState({ date: event.target.value })}
                                            />
                                        </td>
                                    </tr>

                                    <tr>  
                                        <td> <label> Severity: </label> </td>
                                        <td>
                                            < DropdownList
                                                placeholder={this.severityList.name}
                                                options={this.severityList.optionList}
                                                handleDropdown={this.handleDropdown}
                                            />
                                        </td>
                                    </tr>

                                    <tr >
                                        <td > <label> Type: </label> </td>
                                        <td> 
                                            < DropdownList
                                                placeholder={this.typeList.name}
                                                options={this.typeList.optionList}
                                                handleDropdown={this.handleDropdown}
                                            />
                                        </td>
                                    </tr>

                                    <tr>
                                        <td> <label> Region: </label></td>
                                        <td> 
                                            < DropdownList
                                                placeholder={this.regionList.name}
                                                options={this.regionList.optionList}
                                                handleDropdown={this.handleDropdown}
                                            />
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <br /> 
                            <Button animated onClick={e => this.handleBack.bind(this)}>
                                <Button.Content visible> Back </Button.Content>
                                <Button.Content hidden>
                                    <Icon name='arrow left' />
                                </Button.Content>
                            </Button>

                            <Button type="submit" animated>
                                <Button.Content visible>Submit</Button.Content>
                                <Button.Content hidden>
                                    <Icon name='arrow right' />
                                </Button.Content>
                            </Button>
                        </Form>
                    </Grid>
                </Segment> 
                {/* Uncomment below to see state as it gets changed. */}
                {/*  <br />
                    <strong> LEAVE BLANK FOR ALL </strong>
                    <strong> For testing before backend integration </strong>
                    <pre>{JSON.stringify({ severity, date, region, type })}</pre> 
                */}
            </div>
        );
    }
}

export default withRouter(FilterForm);