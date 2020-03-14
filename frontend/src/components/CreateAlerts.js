import React, { Component } from 'react';
import { Dimmer, Loader, Grid, Button, Form, Header, Icon, Segment} from 'semantic-ui-react';
// import DropdownList from "./DropdownList";
import axios from 'axios';
import moment from 'moment';
import FormInputField from './FormInputField';
import createHistory from "history/createBrowserHistory";
const history = createHistory();


class NewCreateAlerts extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loadingData: false,
            properties: {}, 
            requiredProperties: [], 
            payload: {}
        };

        this.apiServer = "https://socnet.pythonanywhere.com/";
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

    handleBack = () => {
        // Soon to be depreciated
        this.props.history.push('/main');
    }

    handleSubmit = async (event) => {
        console.log("event is ", this.inputNode);
        console.log("before payload", this.state.payload);
        event.preventDefault();

        const { payload } = this.state;
        const { history } = this.props;

        console.log(this.state)

        Object.keys(payload).map((payloadKey) => {
            if (payloadKey === "event_severity" && payload[payloadKey].value === undefined) {
                payload[payloadKey] = 'Low';
            } else
                payload[payloadKey] = payload[payloadKey].value;
        });

        payload["event_datetime"] = moment().format("YYYY/MM/DD h:mm:ss");
        console.log("after payload", moment().format("YYYY/MM/DD h:mm:ss"));

        try {
            await axios.post(`${this.apiServer}alerts`, payload);
            history.push('/alerts');
        } catch (e) {
            console.log(e)
        }

    }

    formatItem = (item) => {
        if (item.includes("event")) {
            item = item.substring(6, item.length);
        }
        else {
            item = "sender's name";
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

    severityList = {
        name: "severity",
        type: "dropdown",
        optionList: [{ key: "H", text: "High", value: "high" },
        { key: "L", text: "Low", value: "low" },
        { key: "M", text: "Medium", value: "medium" }]
    };

    firstUpperCase = (label) => {
        return label[0].toUpperCase() + label.slice(1) + ": ";
    }
    render() {
        const { loadingData, properties, errorMessage } = this.state
        const firstUpperCase = this.firstUpperCase;


        if (loadingData) {
            return (
                <Dimmer active inverted>
                    <Loader size="massive">Loading</Loader>
                </Dimmer>
            );
        }

        return (
            <div>
                <Segment basic padded> 
                    <Header as="h1"> Create Alerts </Header> 
                    <Header icon>
                        Please help us stay safe by entering the information about the incident you wish to report.
                    </Header>
                </Segment>
                <Segment padded='very' raised color='teal'>
                    <Grid centered>
                        <Form loading={loadingData} onSubmit={this.handleSubmit.bind(this)} size="large" style={{ width: "60%" }}>
                            <table align="center" className="filters" cellPadding="5px">
                                <tbody>
                                    {Object.keys(properties).map((item) => {
                                        if (item !== "event_datetime") {
                                            return (
                                            <tr>
                                                <td> <label> {this.firstUpperCase(this.formatItem(item))} </label> </td>
                                                <td>
                                                    {/* <input type="date" placeholder="mm/dd/yyyy"/> */}
                                                    <FormInputField required = {properties[item].required}
                                                        type={this.formatType(properties[item].type, properties[item].values)}
                                                        placeholder={properties[item].example}
                                                        propChanged={e => this.propChanged(e, item)}
                                                        values={properties[item].values}
                                                        key={this.formatItem(item)}
                                                        errorMessage={errorMessage}
                                                    />
                                                </td>
                                            </tr>
                                            );
                                        }
                                    })}
                                </tbody>
                            </table>
                            <br />
                            {/* <Button animated onClick={e => this.handleBack.bind(this)}>
                                <Button.Content visible> Back </Button.Content>
                                <Button.Content hidden>
                                    <Icon name='arrow left' />
                                </Button.Content>
                            </Button> */}

                            <Button type="submit" animated>
                                <Button.Content visible>Submit</Button.Content>
                                <Button.Content hidden>
                                    <Icon name='arrow right' />
                                </Button.Content>
                            </Button>
                        </Form>
                    </Grid>
                </Segment>
            </div>
        )
    }
}


export default NewCreateAlerts;