import React, {useState,useEffect} from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import "../styles/Navbar.css";
import API from "../api"; 


const Navbar = () => {
  const user = useSelector((state) => state.auth.user) || JSON.parse(localStorage.getItem("user"));
  const dispatch = useDispatch();

  const [payment, setPayment] = useState(0);
  
 

 
  useEffect(() => {
    const fetchPayment = async () => {
      if (!user) return;
      // In your React component
        console.log("User ID being sent:", user.id);
        console.log("Full user object:", user);
      try {
        const response = await API.get(`/earnings/${user.id}`);
        
        setPayment(response.data.total_earned);
      } catch (error) {alert(error.response.data.detail);
        console.error("Failed to fetch payment:", error);
      }
    };

    fetchPayment();
  }, [user]); 

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    dispatch(logout());
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/dashboard" className="project-name"  >Talent Hive</Link>
      </div>

      <div className="navbar-right">
        {user ? (
          <>
            <span className="earnings">
              {user.role === "client" ? `Spent: ${payment}` : `Earnings: ${payment}`}
            </span>
            <div className="profile-dropdown">
              <button className="profile-btn">{user.name} ▼</button>
              <div className="dropdown-content">
                <Link to="/profile">Profile</Link>
                <button onClick={handleLogout}>Logout</button>
              </div>
            </div>
          </>
        ) : (
          <Link to="/login" className="login-btn">Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
