import React, { useContext, useState }from "react";
import { Route, Routes, Navigate } from 'react-router-dom';
import HomePage from "../HomePage";
import UserListingsPage from "../User/UserListingsPage"
import UserBookingsPage from "../User/UserBookingsPage"

/**
 * Registers routes
 *
 * App => RouteList -> Routes -> {Route, Route....}
 *
 */
function RouteList({signup, login, update}) {
  const username = useContext(userContext)?.username;

  const routesLoggedIn =
   (
      <>
        <Route element={<UserBookingsPage />} path="/bookings" />
        <Route element={<UserListingsPage />} path="/listings" />
        <Route element={<ProfilePage handleSubmit={update}/>} path="/profile" />
      </>
    )

  const routesLoggedOut =
   (
      <>
        <Route element={<SignupForm signup={signup}/>} path="/signup" />
        <Route element={<LoginForm login={login}/>} path="/login" />
      </>
    )

  return (
    <Routes>
      {username ? routesLoggedIn : routesLoggedOut};
      <Route element={<HomePage />} path="/" />
      <Route element={<Navigate to="/"/>} path="*"/>
    </Routes>
  )
}

export default RouteList;