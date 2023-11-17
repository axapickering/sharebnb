import React, { useContext, useState, useEffect } from "react";
import NewListingForm from "../Forms/NewListingForm";
import SpaceList from "../Spaces/SpaceList";
import userContext from "../userContext";
import ShareBnbApi from "../api";
import LoadingSpinner from "../LoadingSpinner";

function UserListingsPage({ submit }) {

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

  if (!listings) return <LoadingSpinner title={"listings"} />;
  if (!listings.length) return <h2>No Listings Found</h2>;

  return <>
    <NewListingForm submit={submit} />
    <SpaceList listings={listings}/>
  </>;
}

export default UserListingsPage;