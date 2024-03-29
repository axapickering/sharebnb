import React from 'react';
/**
 * Alert renders text to show user errors or success upon form submission
 * {LoginForm, SignupForm, ProfilePage} -> Alert
 */
function Alert({ alerts, color }) {
  alerts = Array(alerts);
  return (
    <div className={`alert alert-${ color } mt-3`} role="alert">
      {alerts.map(alert => <p className="m-0" key={alert.m}>{alert}</p>)}
    </div>
  );
}
export default Alert;