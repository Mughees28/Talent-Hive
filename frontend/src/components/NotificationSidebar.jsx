import React from "react";
import "../styles/Dashboard.css";

const NotificationSidebar = ({ notifications }) => {
  return (
    <div className="notification-sidebar">
      <h3>Notifications</h3>
      {notifications.length === 0 ? <p>No new notifications</p> : (
        <ul>
          {notifications.map((notif) => (
            <li key={notif._id}>{notif.message}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default NotificationSidebar;
