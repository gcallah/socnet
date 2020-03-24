import React, { Component } from 'react';
import { Dimmer, Loader, Grid, Button, Form, Header, Icon, Divider, Segment } from 'semantic-ui-react';
import DropdownList from "./DropdownList";
import createHistory from "history/createBrowserHistory";
import { withRouter } from 'react-router-dom';
import "./Filters.css"
import axios from 'axios'

const history = createHistory();

class FilterForm extends Component {
    state = {
        loading: false,
        date: "", 
        severity: [], 
        type: [],
        region: [], 
    };
    
    apiServer = 'https://socnet.pythonanywhere.com/';

    // Sample Input: Development time only
    severityList = {
        name: "severity",
        type: "dropdown",
        optionList: [{key: "H", text: "High", value: "high"}, 
                    {key: "L", text: "Low", value: "low"}, 
                    {key: "M", text: "Medium", value: "medium"}]
    };

    regionList = {
        name: "region", 
        type: "dropdown", 
        optionList: [{key: "NY", text: "NY - New York", value: "NY"}, 
                    { key: "NJ", text: "NJ - New Jersey", value: "NJ" },
                    { key: "CT", text: "CT - Conneticut", value: "CT" }]
    };

    typeList = {
        name: "type",
        type: "dropdown",
        optionList: [{ key: "Fire", text: "Fire", value: "Fire" },
        { key: "Earthquake", text: "Earthquake", value: "Earthquake" },
        { key: "Ransomware", text: "Ransomware", value: "Ransomware" }]
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
        this.props.history.push('/main')
    }

    /// TODO: Merge handleChange with handelSubmit
    // Debugging: Maintaining constant state 
    handleChange = (e, {name, value}) => { 
        this.setState({[name]:value})
    }

    handleValidation = (fields) => {
        if (fields["date"] || fields["severity"].length > 0 || fields["type"].length > 0 || fields["region"].length > 0) {
            console.log("User chose a filter!")
            return true
        } else {
            return false
        }
    }

    handleSubmit = (e) => {
        e.preventDefault()

        const { loading, date, severity, type, region } = this.state
        const apiServer = this.apiServer

        let fields = {
            date: date, 
            severity: severity, 
            type: type, 
            region: region
        };
        
        if (this.handleValidation(fields)) {
            console.log("Form had entries: ", JSON.stringify(fields), typeof(fields))
            try {
                // axios.post({ apiServer }, { fields })
                //     .then(payload => {
                //         console.log("Result form callback: ", payload)
                //         console.log(payload.data)
                
                // this.setState({ loading: true });
                
                axios.get(`${this.apiServer}alerts`)
                .then( payload => { 
                    this.setState({ loading: false });
                    this.props.history.push('/alerts', { alerts: payload.data } ); 
                });

            } catch (e) {
                console.log("ERROR: UNABLE TO FETCH FILTERED RESULTS")
            }
        } else {
            // The user has not added any valid entries to the form
            console.log("The form had no entries. Attempting to load all alerts.")
            try {
                // this.setState({ loading: true });
                axios.get(`${this.apiServer}alerts`)
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
        const { loading, severity, date, region, type } = this.state

        if (loading) {
            return (
                <Dimmer active inverted>
                    <Loader size="massive"> Loading: fetching alerts..</Loader>
                </Dimmer>
            )
        }

        return (
            <div>
                <Segment basic padded> <Header as="h1"> Filter Alerts </Header> </Segment>
                    <Segment padded='very' raised color='teal'>
                        <Grid centered>
                        <Form loading={loading} onSubmit={this.handleSubmit.bind(this)} size="large" style={{ width: "60%" }}>
                            <table align="center" className="filters" cellPadding="5px">
                                <tbody>
                                    {/* Date */}
                                    <tr>
                                        <td> <label> Since (Date): </label>  </td>
                                        <td>
                                            {/* TO-DO: Input type date doesn't work with Safari and IE. */}
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
                    <br />
                    <strong> LEAVE BLANK FOR ALL </strong>
                    <Divider />
                    <strong> For testing before backend integration </strong>
                    <pre>{JSON.stringify({ severity, date, region, type })}</pre>

            </div>
        );
    }
}


export default withRouter(FilterForm);