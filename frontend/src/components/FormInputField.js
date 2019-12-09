import React from 'react';

function FormInputField(props) {
  const {
    label, name, type, placeholder, propChanged
  } = props;
  return (
    <div key={label} className="form-group">
      <div>
        <label
          htmlFor={name}
          className="col-sm-4 col-md-4 col-lg-4"
          key={label}
        >
          {label}
          {' '}
          {' '}
        </label>
        <input
          id={name}
          type={type}
          className="col-md-7"
          style={{ fontSize: '15pt' }}
          placeholder={placeholder}
          name={name}
          onChange={propChanged}
        />
        <br />
      </div>
    </div>
  );
}

export default FormInputField;
