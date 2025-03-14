import React, { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";
import "../styles/PostTask.css";

const PostTask = () => {
  const navigate = useNavigate();
  const [taskData, setTaskData] = useState({
    title: "",
    description: "",
    deadline: "",
    budget: "",
  });

  const handleChange = (e) => {
    setTaskData({ ...taskData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/tasks/createtask", taskData);
      alert("Task posted successfully!");
      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.detail || "Failed to post task.");
    }
  };

  return (
    <div className="post-task-container">
      <h2>Post a Task</h2>
      <form onSubmit={handleSubmit}>
        <label>Task Title</label>
        <input type="text" name="title"  required onChange={handleChange} />
        <label>Task Description</label>
        <textarea name="description" required onChange={handleChange}></textarea>
        <label>Deadline</label>
        <input type="text" placeholder="dd/mm/yyyy" name="deadline" required onChange={handleChange} />
        <label>Budget</label>
        <input type="number" name="budget"  required onChange={handleChange} />
        <button type="submit">Post Task</button>
      </form>
    </div>
  );
};

export default PostTask;
