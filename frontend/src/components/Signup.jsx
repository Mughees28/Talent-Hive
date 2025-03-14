import React, { useState } from "react";
import API from "../api";
import "../styles/Signup.css"; // Import CSS
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    password: "",
    role: "client",
    agency_name: "", // Add agency_name field
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await API.post("/signup", userData);
      
      alert(response.data.message);
      navigate("/login");
      
    } catch (error) {
      alert(error.response.data.detail);
      // alert("Signup failed. Try again.",error);
    }
    finally{
      setIsLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <h2 className="signup-title">Sign Up</h2>
      <form onSubmit={handleSignup} className="signup-form">
        <input type="text" name="name" placeholder="Name" className="signup-input" onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" className="signup-input" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" className="signup-input" onChange={handleChange} required />

        <select name="role" className="signup-input" onChange={handleChange} required>
          <option value="client">Client</option>
          <option value="freelancer">Freelancer</option>
          <option value="agency_owner">Agency Owner</option>
        </select>

        {/* Conditionally Show Agency Name Input */}
        {userData.role === "agency_owner" && (
          <input
            type="text"
            name="agency_name"
            placeholder="Agency Name"
            className="signup-input"
            onChange={handleChange}
            required
          />
        )}

        <button type="submit" className={`signup-button ${isLoading? "loading" : ""}`} disabled={isLoading}>
          {isLoading? "Signing up ...." : "Sign Up" }</button>
      </form>
    </div>
  );
};

export default Signup;
