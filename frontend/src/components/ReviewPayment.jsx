import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api";
import "../styles/ReviewPayment.css";

const ReviewPayment = () => {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const storedUser = JSON.parse(localStorage.getItem("user"));

  const [task, setTask] = useState(null);
  const [isApproved, setIsApproved] = useState(false);
  const [isPaid, setIsPaid] = useState(false);
  const [loading, setLoading] = useState(true);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  useEffect(() => {
    const fetchTaskDetails = async () => {
      try {
        const response = await API.get(`/tasks/${taskId}`);
        setTask(response.data);
        setIsApproved(response.data.is_approved);
        setIsPaid(response.data.is_paid);
      } catch (error) {
        console.error("Error fetching task details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTaskDetails();
  }, [taskId]);

  const handleApproveAndPay = async () => {
    try {
      await API.put(`/tasks/${taskId}/approve`, { is_approved: true });
      await API.post("/payments", {
        task_id: taskId,
        receiver_id: task.assigned_to,
        total_amount: task.selectedbid_amount,
        status: "paid",
      });
      alert("Task approved and payment successful!");
      setIsApproved(true);
      setIsPaid(true);
    } catch (error) {
      console.error("Error processing approval and payment:", error);
      alert("Failed to approve and process payment.");
    }
  };

  const handleReviewSubmit = async () => {
    if (!rating) {
      alert("Please provide a rating.");
      return;
    }

    try {
      await API.post("/reviews", {
        task_id: taskId,
        reviewee_id: task.assigned_to,
        rating,
        comment,
      });
      alert("Review submitted successfully!");
      navigate("/dashboard");
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("Failed to submit review.");
    }
  };

  if (loading) return <p>Loading task details...</p>;
  if (!task) return <p>Task not found.</p>;

  return (
    <div className="review-payment-container">
      <h2>Review & Payment</h2>

     
      <div className="task-details">
        <h3>{task.title}</h3>
        <p><strong>Description:</strong> {task.description}</p>
        <p><strong>Budget:</strong> ${task.budget}</p>
        <p><strong>Amount To Pay:</strong> ${task.selectedbid_amount}</p>
        <p><strong>Status:</strong> {task.status}</p>
      </div>

  
      <div className="submitted-work">
        <h3>Work Submitted</h3>
        <p>{`${task.title}.zip`}</p>
      </div>

      
      {!isApproved && !isPaid ? (
        <div className="approval-section">
          <button onClick={handleApproveAndPay} className="approve-btn">
            Approve & Pay ${task.selectedbid_amount}
          </button>
        </div>
      ) : (
        <>
          <p className="paid-message">Payment completed successfully!</p>

       
          <div className="review-section">
            <h3>Leave a Review</h3>
            <label>Rating:</label>
            <select value={rating} onChange={(e) => setRating(e.target.value)}>
              {[5, 4, 3, 2, 1].map((num) => (
                <option key={num} value={num}>{num} Stars</option>
              ))}
            </select>
            <textarea
              placeholder="Write a comment (optional)"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
            <button onClick={handleReviewSubmit} className="submit-review-btn">Submit Review</button>
          </div>
        </>
      )}
    </div>
  );
};

export default ReviewPayment;
