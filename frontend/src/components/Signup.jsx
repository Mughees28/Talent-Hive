import React, { useState } from "react";
import API from "../api";

const Signup = () => {
  const [userData, setUserData] = useState({
    name: "",
    email: "",
    password: "",
    role: "client",
  });

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await API.post("/signup", userData);
      alert(response.data.message);
    } catch (error) {
      alert("Signup failed. Try again.");
    }
  };

  return (
    <div className="p-5">
      <h2 className="text-xl font-bold">Sign Up</h2>
      <form onSubmit={handleSignup} className="space-y-3">
        <input type="text" name="name" placeholder="Name" className="border p-2 w-full" onChange={handleChange} />
        <input type="email" name="email" placeholder="Email" className="border p-2 w-full" onChange={handleChange} />
        <input type="password" name="password" placeholder="Password" className="border p-2 w-full" onChange={handleChange} />
        <select name="role" className="border p-2 w-full" onChange={handleChange}>
          <option value="client">Client</option>
          <option value="freelancer">Freelancer</option>
          <option value="agency_owner">Agency Owner</option>
        </select>
        <button type="submit" className="bg-blue-500 text-white p-2 w-full">Sign Up</button>
      </form>
    </div>
  );
};

export default Signup;
