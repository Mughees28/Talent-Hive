import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../redux/authslice";
import API from "../api";
import "../styles/Navbar.css";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const user = useSelector((state) => state.auth.user) || JSON.parse(localStorage.getItem("user"));
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [payment, setPayment] = useState(0);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    const fetchPayment = async () => {
      if (!user) return;

      try {
        const response = await API.get(`/payments/earnings/${user.id}`);
        setPayment(response.data.total_earned);
      } catch (error) {
        console.error("Failed to fetch payment:", error);
      }
    };

    fetchPayment();
  }, [user]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    dispatch(logout());
    navigate("/login")
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/dashboard" className="project-name">
          Talent Hive
        </Link>
      </div>

      <div className="navbar-right">
            {user && user.role === "client" && (
            <Link to="/post-task" className="post-task-btn">Post a Task</Link>
            )}

        {user ? (
          <>
            <span className="earnings">
              {user.role === "client" ? `Spent: ${payment}` : `Earnings: ${payment}`}
            </span>

            <div
              className="profile-dropdown"
              onMouseEnter={() => setDropdownOpen(true)}
              onMouseLeave={() => setDropdownOpen(false)}
            >
              <button className="profile-btn">{user.name} 🔽</button>
              {dropdownOpen && (
                <div className="dropdown-content">
                  <Link to="/profile">Profile</Link>
                  <button onClick={handleLogout}>Logout</button>
                </div>
              )}
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
