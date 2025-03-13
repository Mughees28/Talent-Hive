import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import Logout from "./Logout";

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const reduxUser = useSelector((state) => state.auth.user);

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem("user"));
    setUser(storedUser || reduxUser);
  }, [reduxUser]);

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold">Dashboard</h1>
      {user ? (
        <div>
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
          <p>Role: {user.role}</p>
          <Logout />
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Dashboard;
