import { BrowserRouter, Navigate } from 'react-router-dom';
import React, { useEffect, useState } from "react";
import './App.css';
import Navbar from "./Navigation/Navbar"
import RoutesList from "./Navigation/RoutesList"
import userContext from './userContext';
import ShareBnbApi from './api';
import { jwtDecode } from 'jwt-decode';

function App() {

  const [user,setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isLoading, setIsloading] = useState(true)

  useEffect(function () {
    async function fetchUserInfo() {
      if (token) {
        localStorage.setItem("token", token)
        ShareBnbApi.token = token;
        const userInfo = jwtDecode(token);
        try {
          let user = await ShareBnbApi.getUserInfo(userInfo.username);
          setUser(user);
        } catch (err) {
          console.error(err);
        }
      } else {
        localStorage.clear();
        setUser(null);
      }
      setIsloading(false);
    }

    fetchUserInfo();

  }, [token]);

  async function signup(formData) {
    let res = await ShareBnbApi.signup(formData);
    setToken(res.token);
  }

  async function login(formData) {
    let res = await ShareBnbApi.login(formData);
    setToken(res.token);
  }

  return (
    <div>
      <userContext.Provider value={user}>
      <BrowserRouter>
      <Navbar />
    <div className="App container">
      <div className="row">
        <div className="col-9">
        <RoutesList signup={signup} login={login} />
        </div>
      </div>
    </div>
      </BrowserRouter>
      </userContext.Provider>
    </div>
  );
}

export default App;
