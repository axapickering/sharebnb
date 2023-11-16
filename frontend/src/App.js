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
        console.log("token",token);
        localStorage.setItem("token", token)
        ShareBnbApi.token = token;
        const userInfo = jwtDecode(token).sub;
        console.log("userInfo",userInfo);
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
    console.log("signup reached. fdata:",formData)
    let res = await ShareBnbApi.signup(formData);
    console.log("res",res)
    setToken(res['access_token']);
  }

  async function login(formData) {
    console.log("login reached. fdata:",formData)
    let res = await ShareBnbApi.login(formData);
    console.log("res",res)
    setToken(res['access_token']);
  }

  async function edit(formData) {
    let oldData = user
    let newData = await ShareBnbApi.update(formData);
    setUser(newData);
    return {newData, oldData};
  }

  // function that gets user listings and navigates to listings page, passing in user listings as prop

  return (
    <div>
      <userContext.Provider value={user}>
      <BrowserRouter>
      <Navbar />
    <div className="App container">
      <div className="row">
        <div className="col-9">
        <RoutesList signup={signup} login={login} edit={edit} />
        </div>
      </div>
    </div>
      </BrowserRouter>
      </userContext.Provider>
    </div>
  );
}

export default App;
