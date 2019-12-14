import React from 'react';
import { FormControl, InputGroup } from 'react-bootstrap';

function FormInputField(props) {
  const {
    label, type, placeholder, propChanged
  } = props;
  return (
    <InputGroup className="mb-3">
      <InputGroup.Prepend>
        <InputGroup.Text id="basic-addon1">{label}</InputGroup.Text>
      </InputGroup.Prepend>
      <FormControl
        placeholder={placeholder}
        type={type}
        aria-label="Username"
        aria-describedby="basic-addon1"
        onChange={propChanged}
      />
    </InputGroup>
  );
}

export default FormInputField;
