import React, { useContext } from "react";
import userContext from "../userContext";
import { Link } from "react-router-dom";

function Space({ listing, deleteListing, fetchListings }) {

  const { id, title, description, price, address, imageUrl } = listing;

  function handleDelete() {
    deleteListing(id);
    fetchListings();
  }




  const imgStyle = { height: '200px' };

  const displayImg = imageUrl
    ? <img
      className="float-end ms-5 thumbnail"
      style={imgStyle}
      src={imageUrl}
      alt={title}>
    </img>
    : "";

  return (
    <div className="card mb-3">
      <div className="card-body">
        <Link className="text-body text-decoration-none" to={`/spaces/${ id }`}>
          <h6 className="card-title">{title}{displayImg}</h6>
          <p className="card-text"><small>{description}</small></p>
          <p className="card-text"><small>Booking cost: {price}</small></p>
          <p className="card-text"><small>Location: {address}</small></p>
        </Link>
      </div>
      {deleteListing && <button className="btn btn-danger m-1" onClick={handleDelete}>Delete Listing</button>}
    </div>
  );

}

export default Space;