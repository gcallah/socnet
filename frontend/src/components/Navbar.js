import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Menu, Icon } from 'semantic-ui-react';

class NavBar extends Component {
    render() {
        return (
            <Menu pointing secondary>
                <Menu.Item active={true}>
                    <span style={{fontSize: 20}}> 
                        SOCNET
                    </span>
                </Menu.Item>
                    
                <Menu.Menu position='right'>
                    <Menu.Item>
                        <Link to='/createAlert'>
                            <Icon name="add" /> Create Alert
                        </Link>
                    </Menu.Item>

                    <Menu.Item> 
                        <Link to='/'>
                            <Icon name="filter" /> Filter Results
                        </Link>
                    </Menu.Item>
                </Menu.Menu>
            </Menu>
        )
    }
};


export default NavBar;