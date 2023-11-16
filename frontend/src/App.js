import { BrowserRouter, Navigate } from 'react-router-dom';
import React, { useEffect, useState } from "react";
import './App.css';
import Navbar from "./Navigation/Navbar"
import RoutesList from "./Navigation/RoutesList"
import userContext from './userContext';

function App() {

  const [user,setUser] = useState({});

  function signup() {

  }

  function login() {

  }

  return (
    <div className="App container">
      <userContext.Provider value={user}>
      <BrowserRouter>
      <Navbar />
      <div className="row">
        <div className="col-9">
        <RoutesList signup={signup} login={login} />
        </div>
      </div>
      </BrowserRouter>
      </userContext.Provider>
    </div>
  );
}

export default App;
