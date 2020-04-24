import React from 'react';
import { Link } from 'react-router-dom';
import './styles.css';

function Header(props) {
  return (
    <>
      <Link to={ '/' }>
          <h2>{props.title}</h2>
      </Link>
    </>
  )
}

export default Header;