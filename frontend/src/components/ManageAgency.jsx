import React, { useEffect, useState } from "react";
import API from "../api";
import "../styles/ManageAgency.css";

const ManageAgency = () => {
  const storedUser = JSON.parse(localStorage.getItem("user"));
  const [agencyFreelancers, setAgencyFreelancers] = useState([]);
  const [newFreelancer, setNewFreelancer] = useState({ name: "", email: "", skill: "", password: "" });

  useEffect(() => {
    fetchFreelancers();
  }, []);

  const fetchFreelancers = async () => {
    try {
      const response = await API.get("/users/get-freelancer");
      setAgencyFreelancers(response.data.users);
    } catch (error) {
      console.error("Error fetching agency freelancers:", error);
    }
  };

  const handleAddFreelancer = async (e) => {
    e.preventDefault();
    try {
      await API.post("/users/addfreelancer", {
        ...newFreelancer,
        agency_id: storedUser._id,
      });
      alert("Freelancer added successfully!");
      fetchFreelancers();
      setNewFreelancer({ name: "", email: "", skill: "", password: "" });
    } catch (error) {
      console.error("Error adding freelancer:", error);
    }
  };

  const handleRemoveFreelancer = async (freelancerId) => {
    try {
      await API.delete(`/users/deletefreelancer/${freelancerId}`);
      alert("Freelancer removed successfully!");
      fetchFreelancers();
    } catch (error) {
      console.error("Error removing freelancer:", error);
    }
  };

  return (
    <div className="manage-agency">
      {/* Add Freelancer Form */}
      <div className="add-freelancer">
        <h3>Add Freelancer</h3>
        <form onSubmit={handleAddFreelancer}>
          <input
            type="text"
            placeholder="Name"
            value={newFreelancer.name}
            onChange={(e) => setNewFreelancer({ ...newFreelancer, name: e.target.value })}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={newFreelancer.email}
            onChange={(e) => setNewFreelancer({ ...newFreelancer, email: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Skill"
            value={newFreelancer.skill}
            onChange={(e) => setNewFreelancer({ ...newFreelancer, skill: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={newFreelancer.password}
            onChange={(e) => setNewFreelancer({ ...newFreelancer, password: e.target.value })}
            required
          />
          <button type="submit" className="add-btn">Add Freelancer</button>
        </form>
      </div>

      {/* List of Freelancers */}
      <div className="freelancer-list">
        <h3>Current Agency Freelancers</h3>
        <ul>
          {agencyFreelancers.length > 0 ? (
            agencyFreelancers.map((freelancer) => (
              <li key={freelancer._id}>
                {freelancer.name} - {freelancer.skill}
                <button className="remove-btn" onClick={() => handleRemoveFreelancer(freelancer._id)}>
                  Remove
                </button>
              </li>
            ))
          ) : (
            <p>No freelancers added yet.</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ManageAgency;
