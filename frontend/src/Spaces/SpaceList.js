import React, { useContext } from "react";
import userContext from "../userContext";

function SpaceList({ listings }) {
  return <div>
    {listings.map(listing => (<div><h1>{listing.title}</h1></div>))}
  </div>;
}

export default SpaceList;