import Space from "./Space";

function SpaceList({ listings, deleteListing, fetchListings }) {

  if (listings.length === 0) return <p></p>;

  return <div className="m-3">
    {listings.map(listing => (<Space listing={listing} deleteListing={deleteListing} fetchListings={fetchListings} />))}
  </div>;
}

export default SpaceList;