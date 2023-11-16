import React, { useContext } from "react";
import NewListingForm from "../Forms/NewListingForm";

function UserListingsPage({ submit }) {
  return <>
    <NewListingForm submit={submit} />
  </>;
}

export default UserListingsPage;