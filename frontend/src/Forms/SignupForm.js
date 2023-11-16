import React, { useContext, useState } from "react";
import { BrowserRouter, Navigate, useNavigate } from 'react-router-dom';
import userContext from "../userContext";

function SignupForm({ signup }) {

  const initialState = {
    username: "",
    password: "",
    firstName: "",
    lastName: "",
    email: ""
  };

  const navigate = useNavigate();
  const [formData, setFormData] = useState(initialState);

  function handleChange(evt) {
    console.log("formdata",formData);
    const { name , value } = evt.target;
    console.log("new change",name,value);
    setFormData(oldData => ({...oldData,[name]:value}));
  }

  async function handleSubmit(evt) {
    evt.preventDefault();
    try {
      await signup(formData);
      setFormData(initialState);
      navigate("/");
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="mx-auto mt-3" style={{ width: '400px' }}>
      <form onSubmit={handleSubmit}>

        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input className="form-control"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required

          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password"
            className="form-control"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="firstName">First Name</label>
          <input type="firstName"
            className="form-control"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="lastName">Last Name</label>
          <input type="lastName"
            className="form-control"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input type="email"
            className="form-control"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary mt-3">Submit</button>

      </form>
    </div>

  );
}

export default SignupForm;