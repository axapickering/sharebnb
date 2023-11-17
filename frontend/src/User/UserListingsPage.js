import React, { useContext, useState, useEffect } from "react";
import NewListingForm from "../Forms/NewListingForm";
import SpaceList from "../Spaces/SpaceList";
import userContext from "../userContext";
import ShareBnbApi from "../api";
import LoadingSpinner from "../LoadingSpinner";

function UserListingsPage({ submit, deleteListing }) {
  const [showForm, setShowForm] = useState(false);
  const [listings, setListings] = useState(null);
  const { username } = useContext(userContext);



  useEffect(function getListings() {
    fetchUserListings();
  }, []);

  async function fetchUserListings() {
    const userInfo = await ShareBnbApi.getUserInfo(username);
    console.log(userInfo);
    setListings(userInfo.listings);
  }

  function toggleForm() {
    setShowForm(value => !value);
  }

  if (!listings) return <LoadingSpinner title={"listings"} />;

  return <>
    <button onClick={toggleForm} className="btn btn-primary mt-3">Add new listing</button>
    {showForm && <NewListingForm submit={submit} toggleForm={toggleForm} fetchListings={fetchUserListings} />}
    {listings.length ? <SpaceList listings={listings} deleteListing={deleteListing} fetchListings={fetchUserListings} /> : <h2>No Listings Found</h2>}
  </>;
}

export default UserListingsPage;