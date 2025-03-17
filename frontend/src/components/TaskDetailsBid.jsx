import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import API from "../api";
import { useSelector } from "react-redux";
import "../styles/TaskDetailsBid.css";
import "../styles/Profile.css";

const TaskDetailsBid = () => {
  const { taskId } = useParams(); 
  const navigate = useNavigate();
  const storedUser = JSON.parse(localStorage.getItem("user"));
  const reduxUser = useSelector((state) => state.auth.user);
  const [user, setUser] = useState(reduxUser || storedUser);

  const [task, setTask] = useState(null);
  const [bidAmount, setBidAmount] = useState("");
  const [hasBid, setHasBid] = useState(false);
  const [subtasks, setSubtasks] = useState([]); 
  const [allSubtasksCompleted, setAllSubtasksCompleted] = useState(false);
  const [isApproved, setIsApproved] = useState(false); 
  const [waitingForApproval, setWaitingForApproval] = useState(false);


  useEffect(() => {
    const fetchTaskDetails = async () => {
      try {
        const taskResponse = await API.get(`/tasks/${taskId}`);
        setTask(taskResponse.data);
        setIsApproved(taskResponse.data.is_approved); 

        console.log(taskResponse.data.status)

        if (user.role === "agency_owner") {
          const subtaskResponse = await API.get(`/tasks/getsubtask`);
          setSubtasks(subtaskResponse.data.tasks || []);
          
          
         
          const areAllSubtasksCompleted = subtaskResponse.data.tasks.every(subtask => subtask.status === "completed");
          setAllSubtasksCompleted(areAllSubtasksCompleted);
        }

  
        const bidsResponse = await API.get(`/bids/task/${taskId}`);
        const existingBid = bidsResponse.data.find((bid) => bid.bidder_id === user.id);
        if (existingBid) {
          setHasBid(true);
          setBidAmount(existingBid.amount);
        }
      } catch (error) {
        console.error("Error fetching task details:", error);
      }
    };

    fetchTaskDetails();
  }, [taskId, user]);

  const handleBidSubmit = async () => {
    if (!bidAmount) {
      alert("Please enter a bid amount.");
      return;
    }

    try {
      await API.post("/bids", { task_id: taskId, amount: bidAmount });
      alert("Bid submitted successfully!");
      setHasBid(true);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error submitting bid:", error);
      alert("Failed to submit bid.");
    }
  };


  const handleMarkComplete = async () => {
    try {
      await API.put(`/tasks/${taskId}`, { status: "completed" });
      alert("Task marked as completed!");
      if (user.role ==="agency_freelancer"){
        navigate("/dashboard");

      }
      const updatedTask = await API.get(`/tasks/${taskId}`);
      setTask(updatedTask.data);
  
   
      setWaitingForApproval(true);
      setIsApproved(updatedTask.data.is_approved); 
    } catch (error) {
      console.error("Error marking task complete:", error);
      alert("Failed to mark task as complete.");
    }
  };

  if (!task) return <p>Loading task details...</p>;

  return (
    <div className="task-details-container">
  
      <div className="task-details-bid">
        { user.role == "agency_freelancer" ?  "" :<Link to={`/profile/${task.client_id}`} className="profile-link">Client Profile</Link>}
        <h2>{task.title}</h2>
        <p><strong>Description:</strong> {task.description}</p>
        <p><strong>Deadline:</strong> {task.deadline}</p>
        {user.role =="agency_freelancer" ? "" : <p><strong>Budget:</strong> ${task.budget}</p>  }
        <p><strong>Status:</strong> {task.status}</p>

        {task.status === "open" && !hasBid && (user.role === "freelancer" || user.role === "agency_owner") && (
          <div className="bid-section">
            <h3>Place Your Bid</h3>
            <input
              type="number"
              placeholder="Enter bid amount"
              value={bidAmount}
              onChange={(e) => setBidAmount(e.target.value)}
            />
            <button onClick={handleBidSubmit} className="bid-btn">Submit Bid</button>
          </div>
        )}

        {/* {user.role ==="agency_owner"  && (
          <button onClick={handleMarkComplete} className="complete-btn" disabled={!allSubtasksCompleted || task.status === "assigned" || task.status !== "completed" || task.status !== "open"}>
            Mark Task as Complete
          </button>

          
        )} */}
        {user.role === "agency_owner"  && (
          <>
            {task.status === "assigned"  && ( <button
              onClick={handleMarkComplete}
              className="complete-btn"
              disabled={!allSubtasksCompleted || task.status === "completed"}
            >
              {task.status === "completed"  ? "Task Completed" : "Mark Task as Complete"}
            </button>)}
            
            {waitingForApproval && (
              <p className="approval-message">
                Waiting for client approval and payment...
              </p>
            )}
            {isApproved && (
              <Link to={`/task/${taskId}/payment`} className="payment-btn">
                Go to Payment
              </Link>
            )}
          </>
        )}
        {user.role === "freelancer"  && (
          <>
          {task.status ==="assigned" && (
            <button
            onClick={handleMarkComplete}
            className="complete-btn"
            disabled={task.status === "completed"}
          >
            {task.status === "completed" ? "Task Completed" : "Mark Task as Complete"}
          </button>
          ) }
            
            {waitingForApproval && (
              <p className="approval-message">
                Waiting for client approval and payment...
              </p>
            )}
            {isApproved && (
              <Link to={`/task/${taskId}/payment`} className="payment-btn">
                Go to Payment
              </Link>
            )}
          </>
        )}
        {user.role === "agency_freelancer" && task.status === "assigned" && task.status !== "completed" && task.status !== "open" && (
          <button onClick={handleMarkComplete} className="complete-btn" >
            Mark Task as Complete
          </button>
        )}
      
        
      </div>

      
      {user.role === "agency_owner" && task.status === "assigned" && (
        <div className="subtasks-container">
          <h3>Subtasks</h3>
          <ul>
            {subtasks.length > 0 ? (
              subtasks.map((subtask) => (
                <li key={subtask.id} className={subtask.status === "completed" ? "completed-task" : ""}>
                  {subtask.description} - <strong>{subtask.status}</strong>
                </li>
              ))
            ) : (
              <p>No subtasks available.</p>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};

export default TaskDetailsBid;
