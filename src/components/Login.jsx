import { useState } from "react";
export default function Login() {
  // const [email,setEmail] = useState('');
  // const [password,setPassword] = useState('');
  const [enteredValues, setEnteredValues] = useState({
    email: "",
    password: "",
  });
  const [edit,setEdit ] = useState({
    email:false,
    password:false
  })

  const emailIsInvalid = edit.email && !enteredValues.email.includes("@") ;

  function handleInputBlur(identifier){
    setEdit(prevEdit=>({
      ...prevEdit,
      [identifier]:true // computed property names
    }))
  }

  function handleSubmit(event) {
    console.log("Submitted");
    event.preventDefault();
    console.log(enteredValues);
  }

  // function handleEmail(event){

  //   setEmail(event.target.value);
  // }
  // function handlePassword(event){
  //   setPassword(event.target.value)
  // }

  function handleInputChange(identifier, value) {
    setEnteredValues((prevValues) => ({
      ...prevValues,
      [identifier]: value,
    }));
    setEdit(prevEdit=> ({
      ...prevEdit,
      [identifier]:false
    }))
  }
  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>

      <div className="control-row">
        <div className="control no-margin">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            name="email"
            onBlur={()=>handleInputBlur('email')}
            onChange={(event) => handleInputChange("email", event.target.value)}
            value={enteredValues.email}
          />

          <div className="control-error">
            {emailIsInvalid && <p>Please enter a valid email address</p>}
          </div>
        </div>

        <div className="control no-margin">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            name="password"
            onChange={(event) =>
              handleInputChange("password", event.target.value)
            }
            value={enteredValues.password}
          />
        </div>
      </div>

      <p className="form-actions">
        <button className="button button-flat">Reset</button>
        <button className="button">Login</button>
      </p>
    </form>
  );
}
