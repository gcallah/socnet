import React from 'react';
import { FormControl, InputGroup } from 'react-bootstrap';

function FormInputField(props) {
  const {
    label, type, placeholder, propChanged, values
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
        >
          <option key="Choose...">Choose...</option>
          {values.map((value) => {
            return (<option key={value}>{value}</option>);
          })}
        </FormControl>
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
        />
      </InputGroup>
    );
  }
}

export default FormInputField;
