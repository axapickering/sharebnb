import React, { useContext, useState } from "react";
import userContext from "../userContext";
import EditProfileForm from "../Forms/EditProfileForm";

function ProfilePage({ edit }) {

  const [showEditForm,setShowEditForm] = useState(false);
  const { username, firstName, lastName, email } = useContext(userContext);

  function toggleEditForm() {
    setShowEditForm(value => !value);
  }

  return <div>
    <div className="ProfilePage-UserDetails">
      <h2>{firstName} {lastName}</h2>
      <h4>Username: {username}</h4>
      <p>Email: {email}</p>
      <button onClick={toggleEditForm} className="btn btn-primary">Edit</button>
    </div>
    {showEditForm && <EditProfileForm edit={edit}/>}
  </div>
}

export default ProfilePage;