import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api";
import "../styles/ManageAgency.css";

const ManageAgency = () => {
  const storedUser = JSON.parse(localStorage.getItem("user"));
  const [agencyFreelancers, setAgencyFreelancers] = useState([]);
  const [newFreelancer, setNewFreelancer] = useState({ name: "", email: "", skill: "", password: "" });

  const [completedTasks, setCompletedTasks] = useState([]);
  const [subtasks, setSubtasks] = useState([]);
  const [isPaid, setIsPaid] = useState({}); 

  useEffect(() => {
    fetchFreelancers();
    fetchCompletedTasks();
  }, []);

 
  const fetchFreelancers = async () => {
    try {
      const response = await API.get("/users/get-freelancer");
      setAgencyFreelancers(response.data.users);
    } catch (error) {
      console.error("Error fetching agency freelancers:", error);
    }
  };


  const fetchCompletedTasks = async () => {
    try {
      const response = await API.get("/tasks/completed");
  
     
      const tasks = response.data.tasks.filter(task => task.assigned_to === storedUser.id);
      console.log(tasks);
      setCompletedTasks(tasks);
  
    
      fetchSubtasks(tasks);
    } catch (error) {
      console.error("Error fetching completed tasks:", error);
    }
  };
  

  const fetchSubtasks = async (tasks) => {
    try {
      const subtaskResponse = await API.get("/tasks/getsubtask");
      console.log(subtaskResponse);
  
     
      // const relatedSubtasks = subtaskResponse.data.tasks.filter(subtask =>
      //   tasks.some(task => String(task._id) === String(subtask.task_id))
      // );
      const taskIds = new Set(tasks.map(task => String(task._id))); 

      const relatedSubtasks = subtaskResponse.data.tasks.filter(subtask =>
      taskIds.has(String(subtask.task_id)) 
      );
     
  
     
      
      setSubtasks(relatedSubtasks);
  
     
      checkPaymentStatus(relatedSubtasks);
    } catch (error) {
      console.error("Error fetching subtasks:", error);
    }
  };
  

  const checkPaymentStatus = async (subtasks) => {
    const paymentStatus = {};
  
    for (let subtask of subtasks) {
      try {
       
       // const paymentResponse = await API.get(`/payments/task/${subtask.task_id}`);
        let subtaskPaid = subtask.is_paid !== true;
  
        
        paymentStatus[subtask.task_id] = !subtaskPaid;
      } catch (error) {
        console.error("Error checking payment status:", error);
        paymentStatus[subtask.task_id] = true; 
      }
    }
  
    setIsPaid(paymentStatus);
  };
  
 
  const handleAddFreelancer = async (e) => {
    e.preventDefault();
    try {
      await API.post("/users/addfreelancer", {
        ...newFreelancer,
        agency_id: storedUser.id, 
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
      <h2>Manage Agency</h2>

      
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

    
      <div className="freelancer-list">
        <h3>Current Agency Freelancers</h3>
        <ul>
          {agencyFreelancers.length > 0 ? (
            agencyFreelancers.map((freelancer) => (
              <li key={freelancer.id}>
                {freelancer.name} - {freelancer.skill}
                <button className="remove-btn" onClick={() => handleRemoveFreelancer(freelancer.id)}>
                  Remove
                </button>
              </li>
            ))
          ) : (
            <p>No freelancers added yet.</p>
          )}
        </ul>
      </div>

      
      <div className="completed-tasks">
        <h3>Completed Tasks</h3>
        <ul>
          {completedTasks.length > 0 ? (
            completedTasks.map((task) => (
              <li key={task._id}>
                {task.title} - {task.status}
                
                
                {!isPaid[task._id] ? (
                  <Link to={`/agency-payment/${task._id}`} className="pay-btn">
                    Pay Freelancers & Receive Cut
                  </Link>
                ) : (
                  <span className="paid-status">Paid</span>
                )}
              </li>
            ))
          ) : (
            <p>No completed tasks</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ManageAgency;
