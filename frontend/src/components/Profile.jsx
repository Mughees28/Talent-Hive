import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import API from "../api";
import "../styles/Profile.css";

const Profile = () => {
  const { userId } = useParams(); 
  const [user, setUser] = useState(null);
  const [averageRating, setAverageRating] = useState(0);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await API.get(`/users/profile/${userId}`);
        setUser(response.data.user_info);
        setAverageRating(response.data.average_rating);
        setReviews(response.data.reviews);
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };
    fetchProfile();
  }, [userId]);

  if (!user) return <p>Loading profile...</p>;

  return (
    <div className="profile-container">
      <h2>{user.name}</h2>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Role:</strong> {user.role}</p>
      <p><strong>Average Rating:</strong> {averageRating} ⭐</p>

      <h3>Ratings & Reviews</h3>
      {reviews.length > 0 ? (
        <ul className="reviews-list">
          {reviews.map((review) => (
            <li key={review._id} className="review-item">
              <strong>Rating:</strong> {review.rating} ⭐
              <p>{review.comment}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No reviews yet.</p>
      )}
    </div>
  );
};

export default Profile;
