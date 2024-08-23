import { useState } from 'react';

const useInput = (defaultValue, validationFunction) => {
  const [enteredValue, setEnteredValue] = useState(defaultValue);
  const [isTouched, setIsTouched] = useState(false);

  const valueIsValid = validationFunction(enteredValue);
  const hasError = isTouched && !valueIsValid;

  const handleInputChange = (event) => {
    setEnteredValue(event.target.value);
  };

  const handleInputBlur = () => {
    setIsTouched(true);
  };

  const reset = () => {
    setEnteredValue("");
    setIsTouched(false);
  };

  return {
    value: enteredValue,
    isValid: valueIsValid,
    hasError,
    handleInputChange,
    handleInputBlur,
    reset,
  };
};

export default useInput;
