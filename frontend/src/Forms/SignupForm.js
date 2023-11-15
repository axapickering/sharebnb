import React, { useContext } from "react";
import userContext from "../context/userContext";

function SignupForm() {

  const [formData, setFormData] = useState({});

  function handleChange(evt) {
    const { name , value } = evt;
    setFormData(oldData => ({...oldData,[name]:value}));
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    submit(formData);
  }

  return <form onSubmit={handleSubmit}>
    </form>
}

export default SignupForm;