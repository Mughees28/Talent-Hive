import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import TaskStats from "./TaskStats";
import API from "../api";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const storedUser = JSON.parse(localStorage.getItem("user"));
  const reduxUser = useSelector((state) => state.auth.user);
  const [user, setUser] = useState(reduxUser || storedUser);

  // State initialization
  const [taskStats, setTaskStats] = useState({ assigned: 0, completed: 0, posted: 0 });
  const [availableTasks, setAvailableTasks] = useState([]);
  const [assignedTasks, setAssignedTasks] = useState([]);
  const [postedTasks, setPostedTasks] = useState([]);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (!user) return;

    const fetchDashboardData = async () => {
      try {
        let availableResponse, assignedResponse, postedResponse, completedResponse;

        if (user.role === "freelancer" || user.role === "agency_owner") {
          availableResponse = await API.get("/tasks/available");
          assignedResponse = await API.get("/tasks/assigned");
          completedResponse = await API.get("/tasks/completed");
        } else if (user.role === "client") {
          postedResponse = await API.get("/tasks/posted");
          completedResponse = await API.get("/tasks/completed");
          assignedResponse = await API.get("/tasks/assigned");
        } else {
          completedResponse = await API.get("/tasks/completed");
          assignedResponse = await API.get("/tasks/assigned");
        }

        setAvailableTasks(availableResponse?.data?.tasks || []);
        setAssignedTasks(assignedResponse?.data?.tasks || []);
        setPostedTasks(postedResponse?.data?.tasks || []);
        setTaskStats({
          completed: completedResponse?.data?.total_completed || 0,
          assigned: assignedResponse?.data?.total_assigned || 0,
          posted: postedResponse?.data?.total_posted || 0,
        });

      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    };

    fetchDashboardData();
  }, [user]);

  return (
    <div className="dashboard">
      <div className="dashboard-left">
        <h2>Dashboard</h2>
        {user && <TaskStats stats={taskStats} />}

        {/* For Clients: Posted Tasks */}
        {user?.role === "client" && (
          <div className="task-section">
            <h3>Posted Tasks</h3>
            <ul>
              {postedTasks.length > 0 ? (
                postedTasks.map((task) => (
                  <li key={task._id}>
                    <Link to={`/task/${task._id}`} className="task-link">
                      {task.title}
                    </Link> - {task.status}

                    {/* Approve & Pay Button */}
                    {task.status === "completed"  && (
                      <Link to={`/task/${task._id}/payment-review`}>
                        <button className="approve-btn" disabled={task.is_approved && task.is_paid}>
                          {task.is_approved ? "Approved & Paid" : "Approve & Pay"}
                        </button>
                      </Link>
                    )}
                  </li>
                ))
              ) : (
                <p>No posted tasks</p>
              )}
            </ul>
          </div>
        )}

        {/* For Freelancers & Agency Owners */}
        {(user.role === "freelancer" || user.role === "agency_owner") && (
          <div className="task-container">
            {/* Available Tasks */}
            <div className="task-section">
              <h3>Available Tasks</h3>
              <ul>
                {availableTasks.length > 0 ? (
                  availableTasks.map((task) => (
                    <li key={task._id}>
                      <Link to={`/task/${task._id}/bid`} className="task-link">
                        {task.title}
                      </Link> - {task.status}
                    </li>
                  ))
                ) : (
                  <p>No available tasks</p>
                )}
              </ul>
            </div>

            {/* Assigned Tasks */}
            <div className="task-section">
              <h3>Assigned Tasks</h3>
              <ul>
                {assignedTasks.length > 0 ? (
                  assignedTasks.map((task) => (
                    <li key={task._id}>
                      <Link to={`/task/${task._id}/bid`} className="task-link">
                        {task.title}
                      </Link> - {task.status}

                      {/* Show "Breakdown Task" button for agency owners */}
                      {user.role === "agency_owner" && (
                        <Link to={`/task/${task._id}/taskbreakdown`} className="breakdown-btn">
                          Breakdown Task
                        </Link>
                      )}
                    </li>
                  ))
                ) : (
                  <p>No assigned tasks</p>
                )}
              </ul>
            </div>
          </div>
        )}

        {/* For Agency Freelancers: Assigned Tasks Only */}
        {user.role === "agency_freelancer" && (
          <div className="task-container">
            <div className="task-section">
              <h3>Assigned Tasks</h3>
              <ul>
                {assignedTasks.length > 0 ? (
                  assignedTasks.map((task) => (
                    <li key={task._id}>
                      <Link to={`/task/${task._id}/bid`} className="task-link">
                        {task.title}
                      </Link> - {task.status}
                    </li>
                  ))
                ) : (
                  <p>No assigned tasks</p>
                )}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Notifications Sidebar */}
      <div className="dashboard-right">
        <h3>Notifications</h3>
        <ul>
          {notifications.length > 0 ? (
            notifications.map((notif) => <li key={notif.id}>{notif.message}</li>)
          ) : (
            <p>No new notifications</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
