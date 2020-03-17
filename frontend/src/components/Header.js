import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import './styles.css';

function Header(props) {
  return (
    <Fragment>
      <Link to={ '/' }>
        <div>
          <h2>{props.title}</h2>
        </div>
      </Link>
    </Fragment>
  )
}

export default Header