import React, { useContext, useState } from "react";
import userContext from "../userContext";

function LoginForm({ login }) {

  const [formData, setFormData] = useState({});

  function handleChange(evt) {
    const { name , value } = evt;
    setFormData(oldData => ({...oldData,[name]:value}));
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    login(formData);
  }

  return <form onSubmit={handleSubmit}>
    </form>
}

export default LoginForm;