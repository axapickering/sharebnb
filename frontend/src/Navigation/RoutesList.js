import React, { useContext, useState } from "react";
import { Route, Routes, Navigate } from 'react-router-dom';
import HomePage from "../HomePage";
import UserListingsPage from "../User/UserListingsPage";
import UserBookingsPage from "../User/UserBookingsPage";
import userContext from "../userContext";
import ProfilePage from "../User/ProfilePage";
import SignupForm from "../Forms/SignupForm";
import LoginForm from "../Forms/LoginForm";
import SpaceDetailPage from "../Spaces/SpaceDetailPage";


/**
 * Registers routes
 *
 * App => RouteList -> Routes -> {Route, Route....}
 *
 */
function RouteList({ signup, login, edit, submit, deleteListing }) {
  const username = useContext(userContext)?.username;

  const routesLoggedIn =
    (
      <>
        <Route element={<UserBookingsPage />} path="/bookings" />
        <Route element={<UserListingsPage submit={submit} deleteListing={deleteListing} />} path="/listings" />
        <Route element={<ProfilePage edit={edit} />} path="/profile" />
      </>
    );

  const routesLoggedOut =
    (
      <>
        <Route element={<SignupForm signup={signup} />} path="/signup" />
        <Route element={<LoginForm login={login} />} path="/login" />
      </>
    );

  return (
    <Routes>
      {username ? routesLoggedIn : routesLoggedOut};
      <Route element={<HomePage />} path="/" />
      <Route element={<SpaceDetailPage />} path="/spaces/:id" />
      <Route element={<Navigate to="/" />} path="*" />
    </Routes>
  );
}

export default RouteList;