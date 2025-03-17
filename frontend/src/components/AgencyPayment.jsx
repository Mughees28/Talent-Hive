import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api";
import "../styles/AgencyPayment.css";

const AgencyPayment = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const storedUser = JSON.parse(localStorage.getItem("user"));

  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [freelancersPaid, setFreelancersPaid] = useState(false);

  useEffect(() => {
    const fetchTaskDetails = async () => {
      try {
        const taskResponse = await API.get(`/tasks/${taskId}`);
        setTask(taskResponse.data);

        // Fetch subtasks (agency freelancers' work)
        const subtaskResponse = await API.get(`/tasks/getsubtask`);
        const subtasks = subtaskResponse.data.tasks || [];

        // Check if all freelancers are paid
        const allPaid = subtasks.every(subtask => subtask.is_paid === true);
        setFreelancersPaid(allPaid);

      } catch (error) {
        console.error("Error fetching task details:", error);
        setError("Failed to fetch task details.");
      } finally {
        setLoading(false);
      }
    };

    fetchTaskDetails();
  }, [taskId]);

  const handlePayFreelancers = async () => {
    try {
      await API.post(`/payments/agency-payments`, { task_id: taskId });
      alert("Payment to freelancers processed successfully!");
      setFreelancersPaid(true);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error processing payment:", error);
      alert("Failed to process payment.");
    }
  };

  if (loading) return <p>Loading payment details...</p>;
  if (error) return <p>{error}</p>;
  if (!task) return <p>Task not found.</p>;

  const totalAmount = task.selectedbid_amount || 0;
  const agencyCut = (totalAmount * 0.40).toFixed(2);
  const freelancerCut = (totalAmount * 0.60).toFixed(2);

  return (
    <div className="agency-payment-container">
      <h2>Agency Payment</h2>

      <div className="payment-details">
        <h3>{task.title}</h3>
        <p><strong>Total Payment:</strong> ${totalAmount}</p>
        <p><strong>Agency Cut (40%):</strong> ${agencyCut}</p>
        <p><strong>Freelancer Cut (60%):</strong> ${freelancerCut}</p>
      </div>

      {!freelancersPaid ? (
        <button onClick={handlePayFreelancers} className="pay-btn">
          Pay Freelancers
        </button>
      ) : (
        <p className="paid-message">Freelancers have been paid.</p>
      )}
    </div>
  );
};

export default AgencyPayment;
