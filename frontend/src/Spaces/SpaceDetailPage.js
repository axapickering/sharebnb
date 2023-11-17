import React, { useContext, useEffect, useState } from "react";
import userContext from "../userContext";
import { useParams } from "react-router-dom";
import ShareBnbApi from "../api";
import LoadingSpinner from "../LoadingSpinner";

function SpaceDetailPage() {
  const { id } = useParams();
  const [space, setSpace] = useState(null);

  useEffect(function getSpaceOnMount() {
    getSpace(id);
  }, []);

  async function getSpace(id) {
    const currSpace = await ShareBnbApi.getListing(id);
    setSpace(currSpace);
  }

  if (!space) return <LoadingSpinner title="space" />;

  return <div>
    <h1>{space.title}</h1>
    <h1>{space.address}</h1>
    <h1>{space.description}</h1>
    <img src={space.imageUrl} style={{ width: "50%" }} />
    <h1>{space.title}</h1>
  </div>;
}

export default SpaceDetailPage;