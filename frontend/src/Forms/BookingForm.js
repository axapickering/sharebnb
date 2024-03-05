import React, { useContext, useState } from "react";
import { BrowserRouter, Navigate, useNavigate } from 'react-router-dom';
import userContext from "../userContext";
import Alert from "../Alert";

function BookingForm({ createBooking }) {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({});
    const [errors, setErrors] = useState(null);

    function handleChange(evt) {
        const { name, value } = evt.target;
        setFormData(oldData => ({ ...oldData, [name]: value }));
    }

    async function handleSubmit(evt) {
        evt.preventDefault();
        try {
            await createBooking(formData);
            setFormData({ checkIn: "", checkOut: "" });
            navigate("/");
        } catch (err) {
            setErrors('failed to create booking');
        }
    }

    return (
        <div className="mx-auto mt-3" style={{ width: '400px' }}>
            {errors && <Alert alerts={errors} color='danger' />}
            <form onSubmit={handleSubmit}>

                <div className="form-group">
                    <label htmlFor="booking" className="">Check in</label>
                    <input type="date"
                        className="form-control"
                        name="checkIn"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="checkOut" className="">Check Out</label>
                    <input type="date"
                        className="form-control"
                        name="checkOut"
                        value={formData.checkOut}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary mt-3">Create Booking</button>

            </form>
        </div>);
}

export default BookingForm;