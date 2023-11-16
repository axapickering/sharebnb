import React, { useContext, useState } from "react";
import userContext from "../userContext";
import Alert from "../Alert";

function EditProfileForm({ submit }) {

  const [formData, setFormData] = useState({});
  const [alerts, setAlerts] = useState(null);

  function handleChange(evt) {
    const { name , value } = evt;
    setFormData(oldData => ({...oldData,[name]:value}));
  }

  async function handleSubmit(evt) {
    evt.preventDefault();

    try {
        let data = await handleSubmit(formData);
        setFormData(data.newData);
        let dataChanged = [];
        for (let key in data.newData) {
            if (data.newData[key] !== data.oldData[key]) {
                dataChanged.push(` ${key}`);
            }
        }
        if (dataChanged.length > 0) {
            setAlerts({ msgs: [`Sucessfully updated: ${dataChanged}`], color: "success" });
        } else {
            setAlerts(null);
        }

    } catch (err) {
        setAlerts({ msgs: [err], color: "danger" });
    }
  }

  return (
    <div className="mx-auto mt-3" style={{ width: '400px' }}>
        <form onSubmit={handleSubmit}>

            <div className="form-group">
                <label htmlFor="username" className="text-white">Username</label>
                <input className="form-control"
                    name="username"
                    placeholder={formData.username}
                    readOnly
                />
            </div>

            <div className="form-group">
                <label htmlFor="firstName" className="text-white">First Name</label>
                <input type="firstName"
                    className="form-control"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="form-group">
                <label htmlFor="lastName" className="text-white">Last Name</label>
                <input type="lastName"
                    className="form-control"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="form-group">
                <label htmlFor="email" className="text-white">Email</label>
                <input type="email"
                    className="form-control"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
            </div>

            <button type="submit" className="btn btn-primary mt-3">Submit</button>

        </form>
        {alerts && (<Alert alerts={alerts.msgs} color={alerts.color} />)}
    </div>);
}

export default EditProfileForm;