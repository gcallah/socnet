// This file exports a 'Test' class to test functionality in production 
// before pushing it to the main branch

import { Component } from 'react';
import { withRouter } from 'react-router-dom'; 
import axios from 'axios'


class Test extends Component {

    async componentDidMount() {
        try {
            axios.get(`${this.apiServer}filters`)
                .then(payload => {
                    this.setState({ filters: payload.data })
                    this.transformFilterData();
                });
        } catch (e) {
            console.log("Unable to fetch values for the filter form.")
        }
    }

    transformFilterData = () => {
        const payload = this.state.filters.properties;
        // console.log("Before change: ", payload)
        // for ( var field in payload ) {
        //     console.log(typeof(field))
        //     if (field.type === "dropdown") {
        //         var optionList = this.optionListArray(field.optionList)
        //         field.optionList = optionList;
        //     }
        // }
        Object.keys(payload).map((fields) => {
                console.log(fields)
        });
    }

    // optionListArray = (optionObject) => {
    //     console.log("Option List: ", optionObject);
    //     var options = [];
    //     for ( var option in optionObject) {
    //         options.push(option.value());
    //     }
    //     console.log("Options Array:" , options);
    //     return options;
    // }

    return () {}
}

export default withRouter(Test);