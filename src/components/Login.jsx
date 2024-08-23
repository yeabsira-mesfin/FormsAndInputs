import Input from "./Input";
import { isEmail, hasMinLength, isNotEmpty } from "../util/validation";
import { useInput } from "../hooks/useInput";

export default function Login() {
  const {
    value: emailValue,
    handleInputChange: handleEmailChange,
    handleInputBlur: handleEmailBlur,
    hasError: emailHasError,
    reset: resetEmail,
  } = useInput("", (value) => isEmail(value) && isNotEmpty(value));

  const {
    value: passwordValue,
    handleInputChange: handlePasswordChange,
    handleInputBlur: handlePasswordBlur,
    hasError: passwordHasError,
    reset: resetPassword,
  } = useInput("", (value) => hasMinLength(value, 6));

  function handleSubmit(event) {
    event.preventDefault();
    if (emailHasError || passwordHasError) {
      return;
    }
    console.log("Submitted:", emailValue, passwordValue);
  }

  function handleReset() {
    resetEmail();
    resetPassword();
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>

      <div className="control-row">
        <Input
          label="Email"
          id="email"
          type="email"
          name="email"
          required
          onBlur={handleEmailBlur}
          onChange={handleEmailChange}
          value={emailValue}
          error={emailHasError && "Please enter a valid email address!"}
        />
        <Input
          label="Password"
          id="password"
          type="password"
          name="password"
          required
          onBlur={handlePasswordBlur}
          onChange={handlePasswordChange}
          value={passwordValue}
          error={passwordHasError && "Please enter a password greater than 6 characters!"}
        />
      </div>

      <p className="form-actions">
        <button type="button" className="button button-flat" onClick={handleReset}>
          Reset
        </button>
        <button type="submit" className="button">Login</button>
      </p>
    </form>
  );
}
