import React, { Component } from 'react'
import axios from 'axios';
import { Loader, Dimmer, Table, Icon } from 'semantic-ui-react' 
import createHistory from "history/createBrowserHistory"
import { withRouter } from 'react-router-dom';
import config from '../config';
import './styles.css';

const history = createHistory();

class ThreadAlerts extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loadingData: false,
            alerts: [], 
            width: 0
        };
    }
    
    async componentDidMount() {
        // In case we reached this page from the filters first page.
        try {
            this.setState({loadingData: true})
            // console.log("ThreadAlerts.js/ComponentDidMount Props: ", this.props.location.state)
            this.setState({ 
                loadingData: false,
                alerts: this.props.location.state.alerts 
            });
        } catch (e) {  // In case we navigate straight to the main page
            try {
                this.setState({ loadingData: true });
                const payload = await axios.get(`${config.API_URL}alerts`)
                this.setState({
                    loadingData: false,
                    alerts: payload.data
                });
            } catch (e) {
                this.setState({
                    // must put message to the screen here!
                    loadingData: false
                })
                console.log('Error while fetching alerts')
            }
            console.log("Error! " , e , " Alerts State: ", this.state.alerts)
        }
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions.bind(this));
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindowDimensions.bind(this));
    }

    updateWindowDimensions() {
        this.setState({ width: window.innerWidth });
        console.log(this.state.width);
    }

    background = {
        "Low": "#000000",
        "Medium": "#FFCC00",
        "High": "#CC0000",   
    };

    apiServer = 'https://socnet.pythonanywhere.com/';

    renderTableData = (alerts) => {
        alerts.sort((a, b) => {
            let x = a[10],
                y = b[10]
            return x === y ? 0 : x > y ? 1 : -1;
        });

        return alerts.map((alertData) => {

            const id = alertData[0]
            const date = alertData[1]
            const region = alertData[4]
            const title = alertData[6]
            const description = alertData[7]
            const active = alertData[10];
            const icon = active === "Active" ? "check" : "close";
            const bgcolor = this.background;
            
            if (this.state.width > 450) {
                return (
                    <Table.Row
                        onClick={() => {
                            this.props.history.push(`/thread/${id}`)
                        }
                        }>
                        <Table.Cell textAlign="left"> {active} </Table.Cell>
                        <Table.Cell style={{ color: bgcolor[alertData[8]] }}> {title} </Table.Cell>
                        <Table.Cell > {description} </Table.Cell>
                        <Table.Cell> {region} </Table.Cell>
                        <Table.Cell textAlign="right"> {date} </Table.Cell>
                    </Table.Row>
                )
            } else {
                return (
                    <Table.Row
                        onClick={() => {
                            this.props.history.push(`/thread/${id}`)
                        }
                        }>
                        <Table.Cell textAlign="left"> <Icon name={icon} /> </Table.Cell>
                        <Table.Cell style={{ color: bgcolor[alertData[8]] }}> {title} </Table.Cell>
                        <Table.Cell> {region} </Table.Cell>
                        <Table.Cell textAlign="right"> {date} </Table.Cell>
                    </Table.Row>
                )
            }
       
        })
    }

    render() {

        const { loadingData, alerts } = this.state;
        //console.log(alerts);

        if (loadingData) {
            return (
                <Dimmer active inverted>
                    <Loader size="massive"> Loading: fetching alerts..</Loader>
                </Dimmer>
            )
        }

        return (
            <div style={{padding: "2%"}}>
                <Table fixed singleLine padded selectable color="teal">
                    <Table.Header>
                        <Table.HeaderCell> Status </Table.HeaderCell>
                        <Table.HeaderCell> Type </Table.HeaderCell>
                        <Table.HeaderCell width={5} className="hide-mobile"> Description </Table.HeaderCell>
                        <Table.HeaderCell> Region </Table.HeaderCell>
                        <Table.HeaderCell textAlign="right"> Date </Table.HeaderCell>
                    </Table.Header>
                    <Table.Body>
                        { this.renderTableData(alerts) }
                    </Table.Body>
                </Table>
            </div>
        )
    }
}

export default withRouter(ThreadAlerts);
