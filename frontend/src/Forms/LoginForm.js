import React, { useContext, useState } from "react";
import { BrowserRouter, Navigate, useNavigate } from 'react-router-dom';
import userContext from "../userContext";

function LoginForm({ login }) {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState(null);

  function handleChange(evt) {
    const { name , value } = evt.target;
    setFormData(oldData => ({...oldData,[name]:value}));
  }

  async function handleSubmit(evt) {
    evt.preventDefault();
    try {
      await login(formData);
      setFormData({ username: "", password: "" });
      navigate("/");
    } catch (err) {
      setErrors(err);
    }
  }

  return (
    <div className="mx-auto mt-3" style={{ width: '400px' }}>
      <form onSubmit={handleSubmit}>

        <div className="form-group">
          <label htmlFor="username" className="">Username</label>
          <input className="form-control"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password" className="">Password</label>
          <input type="password"
            className="form-control"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary mt-3">Submit</button>

      </form>
      </div>);
}

export default LoginForm;