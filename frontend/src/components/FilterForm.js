import React, { Component } from 'react';
// import { Link } from 'react-router-dom';
// import DatePicker from 'react-date-picker'
import { Grid, Button, Form, Header, Icon, Divider, Segment} from 'semantic-ui-react';
import DropdownList from "./DropdownList";


export default class FilterForm extends Component {
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

    handleDropdown = (name, value) => {
        this.setState({[name]: value}, () => {
            console.log(name, value);
            console.log("Data changed by dropdown")
            console.log(this.state.severity)
        });
    };
    

    // Excecuted when the back button is clicked
    handleBack = () => {
        window.location.href = "/"; // this probably should change
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
        window.location.href = "/";

    }

    render() {
        const { loading, severity, date, region, type } = this.state

        return (
            <div>

                <Segment basic padded> <Header as="h1"> Filter Alerts </Header> </Segment>
                <Segment padded='very' raised color='teal'>
                    <Grid className="center aligned">
                    <Form loading={loading} onSubmit={this.handleSubmit} size="large" style={{width: "60%"}}>
                            <Form.Field>
                                <label> Since (Date)</label>
                                <input type="date" 
                                    onChange={(event) => this.setState({ date: event.target.value })}
                                    value={this.state.date} 
                                />
                            </Form.Field>
                            
                            {/* TO-DO: Write a for loop for this after making 
                                APIs to fetch form properties */}

                            <Form.Field inline >
                                <label > Severity </label>
                                < DropdownList
                                    placeholder={this.severityList.name}
                                    options={this.severityList.optionList}
                                    handleDropdown={this.handleDropdown}
                                />
                            </Form.Field>
                        
                            <Form.Field inline>
                                <label> Region </label>
                                < DropdownList
                                    placeholder={this.severityList.name}
                                    options={this.severityList.optionList}
                                    handleDropdown={this.handleDropdown}
                                />
                            </Form.Field>

                            <Form.Field inline>
                                <label> Type </label>
                                < DropdownList
                                    placeholder={this.severityList.name}
                                    options={this.severityList.optionList}
                                    handleDropdown={this.handleDropdown}
                                />
                            </Form.Field>

                            {/* <Form.Field>
                                <Checkbox label='' />
                            </Form.Field>  */}

                            <Button animated onClick= {e => this.handleBack(e)}>
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
