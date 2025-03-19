import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api";
import "../styles/TaskBreakdown.css";

const TaskBreakdown = () => {
  const { taskId } = useParams(); 
  const navigate = useNavigate();
  const storedUser = JSON.parse(localStorage.getItem("user"));
  
  const [task, setTask] = useState(null);
  const [subtasks, setSubtasks] = useState([]);
  const [agencyFreelancers, setAgencyFreelancers] = useState([]);
  const [newSubtask, setNewSubtask] = useState({ description: "", deadline: "" });
  const [selectedFreelancer, setSelectedFreelancer] = useState("");

  useEffect(() => {
    fetchTaskDetails();
    fetchAgencyFreelancers();
  }, []);

  const fetchTaskDetails = async () => {
    try {
      const response = await API.get(`/tasks/${taskId}`);
      setTask(response.data);
    } catch (error) {
      console.error("Error fetching task details:", error);
    }
  };
  

  const fetchAgencyFreelancers = async () => {
    try {
      const response = await API.get("/users/get-freelancer");
      setAgencyFreelancers(response.data.users);
    } catch (error) {
      console.error("Error fetching freelancers:", error);
    }
  };

  const handleSubtaskSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFreelancer) {
      alert("Please select a freelancer.");
      return;
    }

    try {
      await API.post(`/tasks/addsubtask`, {
        ...newSubtask,
        assigned_to: selectedFreelancer,
        task_id: taskId,
      }
    );

      alert("Subtask created successfully!");
      setNewSubtask({ title: "", description: "", deadline: "" });
      setSelectedFreelancer("")
      fetchTaskDetails(); 
    } catch (error) {
      console.error("Error creating subtask:", error);
      alert("Failed to create subtask.");
    }
  };

  if (!task) return <p>Loading task details...</p>;

  return (
    <div className="task-breakdown">
      <h2>Task Breakdown</h2>
      <div className="task-info">
        <p><strong>Title:</strong> {task.title}</p>
        <p><strong>Description:</strong> {task.description}</p>
        <p><strong>Deadline:</strong> {task.deadline}</p>
        <p><strong>Budget:</strong> ${task.budget}</p>
      </div>

      <div className="subtask-form">
        <h3>Create a Subtask</h3>
        <form onSubmit={handleSubtaskSubmit}>
          <input
            type="text"
            placeholder="Subtask Title"
            value={newSubtask.title}
            onChange={(e) => setNewSubtask({ ...newSubtask, title: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Subtask Description"
            value={newSubtask.description}
            onChange={(e) => setNewSubtask({ ...newSubtask, description: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="dd/mm/yyyy"
            value={newSubtask.deadline}
            onChange={(e) => setNewSubtask({ ...newSubtask, deadline: e.target.value })}
            required
          />
          <select 
            value={selectedFreelancer} 
            onChange={(e) => setSelectedFreelancer(e.target.value)} 
            required
          >
            <option value="">Assign to Freelancer</option>
            {agencyFreelancers.map((freelancer) => (
              <option key={freelancer._id} value={freelancer._id}>
                {freelancer.name}
              </option>
            ))}
          </select>
          <button type="submit" className="submit-btn">Create Subtask</button>
        </form>
      </div>
    </div>
  );
};

export default TaskBreakdown;
