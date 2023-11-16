import React, { useContext, useState } from "react";
import userContext from "../userContext";

function SignupForm({ signup }) {

  const [formData, setFormData] = useState({});

  function handleChange(evt) {
    const { name , value } = evt;
    setFormData(oldData => ({...oldData,[name]:value}));
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    signup(formData);
  }

  return <form onSubmit={handleSubmit}>
    </form>
}

export default SignupForm;