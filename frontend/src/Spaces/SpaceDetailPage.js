import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ShareBnbApi from "../api";
import LoadingSpinner from "../LoadingSpinner";
import BookingForm from "../Forms/BookingForm";
import Alert from "../Alert";

function SpaceDetailPage() {
  const { id } = useParams();
  const [space, setSpace] = useState(null);
  const [errors, setErrors] = useState(null);

  useEffect(function getSpaceOnMount() {
    getSpace(id);
  }, []);

  async function getSpace(id) {
    const currSpace = await ShareBnbApi.getListing(id);
    setSpace(currSpace);
  }

  async function createBooking(formData) {
    try {
      await ShareBnbApi.createBooking({
        space_id: space.id,
        price: space.price,
        check_in: formData.checkIn,
        check_out: formData.checkOut,
      });
    } catch(err) {
      setErrors(err)
    }
  }

  if (!space) return <LoadingSpinner title="space" />;

  return <div>
    <h1 className="mt-4">{space.title}</h1>
    <h2>Address: {space.address}</h2>
    <img className="my-3 border border-white border-4 rounded"
      alt={`for ${space.id}`}
      src={space.imageUrl}
      style={{ width: "50%" }} />
    <h3>description</h3>
    <p className="text-white-50">{space.description}</p>
    {errors && <Alert alerts={errors} color='danger' />}
    <BookingForm createBooking={createBooking} />
  </div>;
}

export default SpaceDetailPage;