import React, { useEffect, useState } from 'react';
import SpaceList from "./Spaces/SpaceList";
import ShareBnbApi from './api';
import LoadingSpinner from './LoadingSpinner';

function HomePage() {
  const [listings, setListings] = useState(null);

  useEffect(function getListings() {
    fetchListings();
  }, []);

  async function fetchListings(term) {
    const listingsArray = await ShareBnbApi.getListings(term);
    setListings(listingsArray);
  }

  if (!listings) return <LoadingSpinner title={"listings"} />;
  if (!listings.length) return <h2>No Listings Found</h2>;

  return (
    <div>
      <SpaceList listings={listings} />
    </div>
  );
}

export default HomePage;