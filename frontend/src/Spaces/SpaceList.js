import React, { useContext } from "react";
import userContext from "../userContext";
import Space from "./Space";

function SpaceList({ listings }) {

  if (listings.length === 0) return <p></p>

  return <div className="m-3">
    {listings.map(listing => (<Space listing={listing}/>))}
  </div>;
}

export default SpaceList;