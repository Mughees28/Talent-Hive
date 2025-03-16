import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api";
import "../styles/TaskDetails.css";
import { Link } from "react-router-dom";
import "../styles/Profile.css";

const TaskDetails = () => {
  const { taskId } = useParams(); // Get task ID from URL
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [bids, setBids] = useState([]);
  const [selectedBid, setSelectedBid] = useState("");
  const [amount, setSelectedBidAmount] = useState("");

  useEffect(() => {
    const fetchTaskDetails = async () => {
      try {
        const taskResponse = await API.get(`/tasks/${taskId}`);
        setTask(taskResponse.data);

        const bidsResponse = await API.get(`/bids/task/${taskId}`);
        setBids(bidsResponse.data);
      } catch (error) {
        console.error("Error fetching task details:", error);
      }
    };

    fetchTaskDetails();
  }, [taskId]);

  const handleAssignTask = async () => {
    if (!selectedBid) {
      alert("Please select a bid to assign.");
      return;
    }

    try {
      await API.put(`/tasks/${taskId}`, { assigned_to: selectedBid,status:"assigned", selectedbid_amount: amount });
      alert("Task successfully assigned!");
      navigate("/dashboard");
    } catch (error) {
      console.error("Error assigning task:", error);
      alert("Failed to assign task.");
    }
  };

  if (!task) return <p>Loading task details...</p>;

  return (
    <div className="task-details">
      <h2>{task.title}</h2>
      <p><strong>Description:</strong> {task.description}</p>
      <p><strong>Deadline:</strong> {task.deadline}</p>
      <p><strong>Budget:</strong> ${task.budget}</p>

      <h3>Bids:</h3>
      {bids.length > 0 ? (
        <ul className="bid-list">
          {bids.map((bid) => (
            <li key={bid._id}>
        
              <p>
                <strong>Bidder:</strong> 
                <Link to={`/profile/${bid.bidder_id}`} className="profile-link">
                    {bid.name}
                </Link>
                </p>
              <p><strong>Amount:</strong> ${bid.amount}</p>
              <input
                type="radio"
                name="selectedBid"
                value={bid.bidder_id}
                onChange={() =>{ setSelectedBid(bid.bidder_id);
                                setSelectedBidAmount(bid.amount)
                }
                }
              />
            </li>
          ))}
        </ul>
      ) : (
        <p>No bids yet.</p>
      )}

      <button onClick={handleAssignTask} disabled={!selectedBid} className="assign-btn">
        Assign Task
      </button>
    </div>
  );
};

export default TaskDetails;
