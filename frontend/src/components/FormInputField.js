import React from 'react';
import { FormControl, InputGroup } from 'react-bootstrap';

function FormInputField(props) {
  const {
    label, type, placeholder, propChanged, values, errorMessage
  } = props;
  if (typeof values !== "undefined") {
    return (
      <InputGroup className="mb-3">
        <InputGroup.Prepend>
          <InputGroup.Text id="basic-addon1">{label}</InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl
          placeholder={placeholder}
          as={type}
          onChange={propChanged}
          required
        >
          <option key="Choose...">Choose...</option>
          {values.map((value) => {
            return (<option key={value}>{value}</option>);
          })}
        </FormControl>
        <div>{errorMessage}</div>
      </InputGroup>
    );
  } else {
    return (
      <InputGroup className="mb-3">
        <InputGroup.Prepend>
          <InputGroup.Text id="basic-addon1">{label}</InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl
          placeholder={placeholder}
          type={type}
          onChange={propChanged}
          required
        />
      </InputGroup>
    );
  }
}

export default FormInputField;
