import React, { useState } from "react";


/**  */
function NewListingForm({ submit, toggleForm, fetchListings }) {
  const initialFormData = {
    title: "",
    description: "",
    price: 0,
    address: "",
    image: null
  };

  const [formData, setFormData] = useState(initialFormData);

  /** handles change of input fields of form*/
  function handleChange(evt) {
    const { name, value } = evt.target;
    setFormData(oldData => ({ ...oldData, [name]: value }));
  }

  /** handles file field of form*/
  function handleFile(evt) {
    const file = evt.target.files[0];
    setFormData(oldData => ({ ...oldData, "image": file }));
  }

  /** handles submission of form*/
  async function handleSubmit(evt) {
    evt.preventDefault();
    await submit(formData);
    toggleForm();
    fetchListings();
  }

  return (
    <div className="mx-auto mt-3" style={{ width: '400px' }}>
      <form onSubmit={handleSubmit}>

        <div className="form-group">
          <label htmlFor="title">title</label>
          <input className="form-control"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required

          />
        </div>

        <div className="form-group">
          <label htmlFor="description">description</label>
          <input type="description"
            className="form-control"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="price">price</label>
          <input type="number"
            className="form-control"
            name="price"
            value={formData.price}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="address">address</label>
          <input type="address"
            className="form-control"
            name="address"
            value={formData.address}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="Image">Image</label>
          <input type="file"
            className="form-control"
            name="image"
            onChange={handleFile}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary mt-3">Submit</button>

      </form>
    </div>

  );
}

export default NewListingForm;