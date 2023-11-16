import React, { useContext } from "react";
import { Link } from "react-router-dom";
import userContext from "../context/userContext";

/**
 * Renders Nav bar Links depending on if user is logged in
 *
 * App -> Navbar -> {Link,...}
 */
function Navbar() {

  function navUserLoggedIn() {
    return (
      <ul className="navbar-nav me-auto mb-2 mb-lg-0 ">
        <li className="nav-item nav-link">
          <Link className="nav-link" aria-current="page" to={`/bookings`}>Bookings</Link>
        </li>
        <li className="nav-item nav-link">
          <Link className="nav-link" aria-current="page" to={`/listings`}>My Listings</Link>
        </li>
        <li className="nav-item nav-link">
          <Link className="nav-link" aria-current="page" to={`/profile`}>Profile</Link>
        </li>
        <li className="nav-item nav-link">
          <Link onClick={logout} className="nav-link" aria-current="page" to={`/`}>Logout: {username}</Link>
        </li>
      </ul>
    );
  }


  /**Returns JSX for nav bar links if a user is not logged in */
  function navUserLoggedOut() {
    return (
      <ul className="navbar-nav me-auto mb-2 mb-lg-0 ">
        <li className="nav-item nav-link">
          <Link className="nav-link" aria-current="page" to={`/login`}>Login</Link>
        </li>
        <li className="nav-item nav-link">
          <Link className="nav-link" aria-current="page" to={`/signup`}>Sign Up</Link>
        </li>
      </ul>
    );
  }

  return (
    <nav className="navbar navbar-expand-lg " style={{backgroundColor: "#ccbcac"}}>
      <div className="container-fluid">
        <Link className="navbar-brand" to={`/`}>ShareBnB</Link>
        <div id="navbarSupportedContent">
          {username ? navUserLoggedIn() : navUserLoggedOut()}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;