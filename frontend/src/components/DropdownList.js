import React, { Component } from 'react'
import { Dropdown } from 'semantic-ui-react'

// The module requires three props:
// // placeholder: identify the dropdown menu
// // options: array of dropdown options structured as {key, name, value}
// // handleDropdown: a handler function which accepts the selcted values 

class DropdownList extends Component {
    state = {
        isFetching: false,  // animates a spinning wheel during search
        multiple: true, 
        search: true, 
        value: [] 
    };
    
    // Maintain the state as the user changes the selection(s).
    handleChange = (e, { value }) => {
        this.setState({ value })
        // console.log(this.state.value)
    };

    // Once the dropdown is closed, the control is packed back 
    // to a handler. placeholder is used as an identifier and 
    // value holds the dropdown selections (empty array if no selections)
    handleClose = (e, {value}) => {
        //console.log(this.state.value);
        //console.log("Name", this.props.placeholder)
        this.props.handleDropdown(this.props.placeholder, this.state.value)
    };

    render() {
        const { isFetching, multiple, search, value  } = this.state
        return (
            <Dropdown 
                fluid
                selection
                disabled = {isFetching}
                loading = {isFetching}
                multiple = {multiple}
                search = {search}
                placeholder={"Select " + this.props.placeholder}
                options = {this.props.options} 
                noResultsMessage = "No results found."
                onChange={this.handleChange}
                onClose = {this.handleClose}
                selectOnNavigation={false}
                value = {value}
            />
        )
    }
}

export default DropdownList;