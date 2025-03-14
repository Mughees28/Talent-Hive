import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import TaskStats from "./TaskStats";
import API from "../api";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const user = useMemo(() => reduxUser || JSON.parse(localStorage.getItem("user")), [reduxUser]);  
  // Correct state initialization
  const [taskStats, setTaskStats] = useState({ assigned: 0, completed: 0, posted: 0 });
  const [tasks, setTasks] = useState([]);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (!user) return;

    const fetchDashboardData = async () => {
      try {
        let tasksResponse, completedResponse, assignedResponse, postedResponse, notificationsResponse;

        if (user.role === "freelancer" || user.role === "agency_owner") {
          tasksResponse = await API.get("/tasks/posted");
          completedResponse = await API.get("/tasks/completed");
          assignedResponse = await API.get("/tasks/assigned");
        } else if (user.role === "client") {
          tasksResponse = await API.get("/tasks/posted");
          completedResponse = await API.get("/tasks/completed");
          postedResponse = await API.get("/tasks/posted");
        }

        // notificationsResponse = await API.get("/notifications");

        setTasks(tasksResponse?.data?.tasks || []);
        setTaskStats({
          completed: completedResponse?.data?.total_completed || 0,
          assigned: assignedResponse?.data?.total_assigned || 0,
          posted: postedResponse?.data?.total_posted || 0,
        });
        setNotifications(notificationsResponse?.data?.notifications || []);
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

        <div className="task-section">
          <h3>{user?.role === "client" ? "Posted Tasks" : "Available Tasks"}</h3>
          <ul>
            {tasks.length > 0 ? tasks.map((task) => <li key={task._id}>{task.title} - {task.status}</li>) : <p>No tasks available</p>}
          </ul>
        </div>
      </div>

      <div className="dashboard-right">
        <h3>Notifications</h3>
        <ul>
          {notifications.length > 0 ? notifications.map((notif) => <li key={notif.id}>{notif.message}</li>) : <p>No new notifications</p>}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
