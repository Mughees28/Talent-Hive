import React from "react";
import "../styles/Dashboard.css";

const TaskList = ({ title, tasks }) => {
  return (
    <div className="task-list">
      <h3>{title}</h3>
      {tasks.length === 0 ? <p>No tasks available</p> : (
        <ul>
          {tasks.map((task) => (
            <li key={task._id}>
              <strong>{task.title}</strong> - <span>{task.status}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;
