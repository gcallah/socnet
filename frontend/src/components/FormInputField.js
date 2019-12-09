import React from 'react';

function FormInputField(props) {
  const {
    label, name, type, placeholder,
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
          className="col-sm-2 col-md-2 col-lg-2"
          style={{ fontSize: '15pt' }}
          placeholder={placeholder}
          name={name}
        />
        <br />
      </div>
    </div>
  );
}

export default FormInputField;
