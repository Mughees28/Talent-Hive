import React from "react";
import "../styles/Dashboard.css";

const TaskStats = ({ stats }) => {
  return (
    <div className="task-stats">
      <div className="stat-box">Assigned: {stats.assigned}</div>
      <div className="stat-box">Completed: {stats.completed}</div>
      <div className="stat-box">In Progress: {stats.posted}</div>
    </div>
  );
};

export default TaskStats;
