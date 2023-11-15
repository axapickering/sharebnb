import React, { useContext, useState } from "react";
import userContext from "../context/userContext";

function EditProfileForm({ submit }) {

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

export default EditProfileForm;