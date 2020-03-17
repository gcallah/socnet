import React, { Component } from 'react'
import { Dropdown } from 'semantic-ui-react'

class DropdownList extends Component {
    state = {
        isFetching: false, 
        multiple: true, 
        search: true, 
        value: []
    };
    
    handleChange = (e, { value }) => {
        this.setState({ value })
        console.log(this.state.value)
    };

    handleClose = (e, {value}) => {
        console.log(this.state.value);
        console.log("Name", this.props.placeholder)
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