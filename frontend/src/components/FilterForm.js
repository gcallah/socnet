import React, { Component } from 'react';
import { Grid, Button, Form, Header, Icon, Divider, Segment } from 'semantic-ui-react';
import DropdownList from "./DropdownList";
import createHistory from "history/createBrowserHistory";
import { withRouter } from 'react-router-dom';
import "./Filters.css"

const history = createHistory();

class FilterForm extends Component {
    state = {
        loading: false,
        severity: [], 
        date: '', 
        region: [], 
        type: [],
        //properties: {}
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
                    { key: "NY", text: "CT - Conneticut", value: "CT" }]
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

    handleSubmit = () => {
        const { loading, field1, field2, field3, field4 } = this.state
        this.setState({ severity: field1, date: field2, region: field3, type: field4 })

        // for now as there is no functionality in the API
        this.props.history.push('/main')
    }

    render() {
        const { loading, severity, date, region, type } = this.state

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
                                                value={this.state.date}
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